"""LLM tool-calling simulation (Section 13B)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 13B: LLM TOOL-CALLING SIMULATION (structured output, no real API)
# ==============================================================================
#
# A small, fully offline demonstration of the "LLM tool calling" /
# "function calling" pattern that real LLM APIs support natively: the
# model is given a list of available tools (name, description,
# parameters) in its prompt, asked to respond with a structured JSON
# object naming which tool to call and with what arguments, and the
# CALLING CODE (not the model) actually executes it. This class handles
# the second half - parsing a JSON tool-call response and dispatching
# it to a real Python callable - and can be driven either by a genuine
# LLMConnector reply (when configured) or by feeding it hand-written
# JSON directly, which is how DEMO_TOOL_CALL_EXAMPLES below exercises
# it with zero network dependency.

TOOL_DEFINITIONS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a named place.",
        "parameters": {"place": "string, e.g. 'Berlin' or 'Nairobi'"},
    },
    {
        "name": "convert_currency",
        "description": "Convert an amount from one currency to another.",
        "parameters": {"amount": "number", "from_currency": "3-letter code", "to_currency": "3-letter code"},
    },
    {
        "name": "get_trivia",
        "description": "Fetch a trivia question, optionally at a given difficulty.",
        "parameters": {"difficulty": "optional, one of 'easy'/'medium'/'hard'"},
    },
    {
        "name": "search_memory",
        "description": "Search the user's remembered facts for a query.",
        "parameters": {"query": "string"},
    },
    {
        "name": "define_word",
        "description": "Look up the dictionary definition of a word.",
        "parameters": {"word": "string"},
    },
]


def _build_tool_calling_system_prompt() -> str:
    """Builds the system prompt describing available tools, in the
    plain-JSON-schema style most LLM providers expect when NOT using
    their native tool-calling API parameter (kept dependency-light,
    same philosophy as everything else calling out to an LLM in this
    file - see LLMConnector, Section 6I)."""
    tool_lines = []
    for tool in TOOL_DEFINITIONS:
        params_desc = ", ".join(f"{k} ({v})" for k, v in tool["parameters"].items())
        tool_lines.append(f"- {tool['name']}({params_desc}): {tool['description']}")
    tools_block = "\n".join(tool_lines)
    return (
        "You have access to these tools:\n" + tools_block + "\n\n"
        "If the user's request needs one of these tools, respond with "
        "ONLY a JSON object: {\"tool\": \"<name>\", \"arguments\": {...}}. "
        "If no tool is needed, respond normally with plain text instead."
    )


PROMPT_TEMPLATES["tool_calling"] = {"system": _build_tool_calling_system_prompt()}


class ToolCallParser:
    """
    Parses a (hopefully) structured JSON tool-call response and
    dispatches it to a real Python callable registered for that tool
    name. Fails closed at every stage: malformed JSON, an unknown tool
    name, or a handler that raises are all caught and turned into a
    plain-text error rather than propagating - a bad or unexpected LLM
    response should never crash the bot.
    """

    def __init__(self):
        self.handlers = {}  # tool_name -> callable(**kwargs) -> str

    def register(self, tool_name: str, handler):
        if tool_name not in {t["name"] for t in TOOL_DEFINITIONS}:
            raise ValueError(f"'{tool_name}' isn't a declared tool in TOOL_DEFINITIONS")
        self.handlers[tool_name] = handler

    @staticmethod
    def looks_like_tool_call(text: str) -> bool:
        """Quick, cheap check before attempting a full JSON parse -
        avoids paying json.loads' cost on the common case of an
        ordinary plain-text reply that was never meant to be a tool
        call."""
        stripped = text.strip()
        return stripped.startswith("{") and '"tool"' in stripped

    def parse(self, text: str):
        """Returns (tool_name, arguments_dict) or None if `text` isn't
        a valid, well-formed tool call."""
        if not self.looks_like_tool_call(text):
            return None
        try:
            data = json.loads(text.strip())
        except json.JSONDecodeError:
            return None
        if not isinstance(data, dict) or "tool" not in data:
            return None
        tool_name = data.get("tool")
        arguments = data.get("arguments", {})
        if not isinstance(arguments, dict):
            return None
        return tool_name, arguments

    def dispatch(self, text: str):
        """
        Full pipeline: parse `text` as a tool call, look up the
        registered handler, call it, and return its string result - or
        None at any failure point (not a tool call, unknown tool, no
        handler registered, or the handler itself raised), so callers
        can fall through to treating `text` as an ordinary reply.
        """
        parsed = self.parse(text)
        if parsed is None:
            return None
        tool_name, arguments = parsed
        handler = self.handlers.get(tool_name)
        if handler is None:
            return None
        try:
            return handler(**arguments)
        except TypeError:
            return f"(tool call to '{tool_name}' had missing/invalid arguments)"
        except Exception as e:
            return f"(tool call to '{tool_name}' failed: {e})"


# A handful of hand-written EXAMPLE tool-call payloads, formatted exactly
# the way an LLM following PROMPT_TEMPLATES["tool_calling"] would be
# expected to respond. These aren't fetched from anywhere and don't
# involve any real LLM call - they exist purely so ToolCallParser's
# parsing/dispatching logic can be exercised deterministically and
# offline (see run_tool_call_demo() below and its use in the self-test),
# without needing a live LLM connection just to prove the plumbing works.
DEMO_TOOL_CALL_EXAMPLES = [
    '{"tool": "get_weather", "arguments": {"place": "Tokyo"}}',
    '{"tool": "convert_currency", "arguments": {"amount": 25, "from_currency": "GBP", "to_currency": "JPY"}}',
    '{"tool": "get_trivia", "arguments": {"difficulty": "medium"}}',
    '{"tool": "search_memory", "arguments": {"query": "favorite food"}}',
    '{"tool": "define_word", "arguments": {"word": "ephemeral"}}',
    "Just a normal conversational reply, not a tool call at all.",
    '{"tool": "not_a_real_tool", "arguments": {}}',
    '{"tool": "get_weather", "arguments": {"wrong_param": "oops"}}',
    "{not even valid json",
]


def run_tool_call_demo(bot: "ChatBot") -> str:
    """
    Runs every example in DEMO_TOOL_CALL_EXAMPLES through bot.
    tool_call_parser.dispatch() and reports what happened for each -
    a real tool call and result, "not a tool call" (plain text was
    correctly left alone), or a specific failure mode (unknown tool,
    bad arguments, malformed JSON). Useful both as a sanity check
    after changing TOOL_DEFINITIONS/registered handlers, and as a
    concrete illustration of how the LLM tool-calling simulation
    (Section 13B) behaves on every kind of input it might see.
    """
    lines = ["TOOL-CALL PARSER DEMO", ""]
    for example in DEMO_TOOL_CALL_EXAMPLES:
        parsed = bot.tool_call_parser.parse(example)
        if parsed is None:
            if bot.tool_call_parser.looks_like_tool_call(example):
                lines.append(f"  [malformed]     {example[:50]}")
            else:
                lines.append(f"  [not a call]    {example[:50]}")
            continue
        tool_name, _arguments = parsed
        result = bot.tool_call_parser.dispatch(example)
        if result is None:
            lines.append(f"  [unknown tool]  {tool_name}")
        elif result.startswith("(tool call"):
            lines.append(f"  [call failed]   {tool_name} -> {result}")
        else:
            preview = result.splitlines()[0][:60] if result else ""
            lines.append(f"  [dispatched]    {tool_name} -> {preview}...")
    return "\n".join(lines)




# ==============================================================================
