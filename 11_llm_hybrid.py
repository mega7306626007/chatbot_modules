"""LLM hybrid connector + caching/cost/PII/context-window extensions (Section 6I + EXTs)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 6I: LLM HYBRID CONNECTOR (optional, opt-in, real generation)
# ==============================================================================
#
# Everything else in this file - the strict regex engine, the keyword
# matcher, the three neural networks - can only SELECT from a fixed set
# of pre-written replies or trained intent labels. None of them can
# produce a genuinely new sentence. LLMConnector is the one component
# that can: it's a thin, dependency-free client for a real LLM API
# (Claude), used as a LAST-RESORT fallback for messages nothing else
# understood, so the bot can respond sensibly to things that were never
# anticipated in its fixed vocabulary - the one thing a classifier,
# however well-trained, structurally cannot do.
#
# This is OFF BY DEFAULT and stays fully optional:
#   - Requires an internet connection (everything else in this file
#     works fully offline; this is the one exception).
#   - Requires a real Anthropic API key, supplied by the USER via a
#     local config file (chatbot_llm_config.json) they edit by hand -
#     never hardcoded, never bundled, never sent anywhere but to
#     Anthropic's API directly from the user's own device.
#   - Requires the user to explicitly set "enabled": true in that file.
#   - This is a PAID API - check current Anthropic pricing before
#     enabling, since every fallback message sent this way costs money.
#
# Implemented with Python's built-in urllib rather than the official
# anthropic SDK, specifically so no extra `pip install` is needed
# beyond what Pydroid 3 already has - one less thing that can go wrong
# on a phone.
#
# FAILS CLOSED, ALWAYS: any problem at any stage - missing config,
# disabled, invalid/missing key, no network, timeout, malformed
# response, rate limiting - returns None rather than raising, and the
# chatbot's existing offline fallback chain (NN classifier -> TF-IDF
# similarity match -> generic "I don't understand") takes over exactly
# as it did before this section existed. The LLM is additive, never
# load-bearing.

LLM_CONFIG_TEMPLATE = {
    "_instructions": (
        "Set 'provider' to either 'anthropic' or 'openai', fill in the "
        "matching 'api_key' for that provider, then set 'enabled' to "
        "true and save this file. Anthropic keys start with 'sk-ant-' "
        "(get one at https://console.anthropic.com/settings/keys); "
        "OpenAI keys start with 'sk-' (get one at "
        "https://platform.openai.com/api-keys). Both are PAID APIs - "
        "check current pricing before enabling. Once a key is saved "
        "here, you can switch providers from inside the chat itself by "
        "typing 'change to gpt' or 'change to claude' - no need to "
        "re-edit this file just to switch which model is active. "
        "Never share this file or your key with anyone, and never "
        "commit it to source control."
    ),
    "enabled": False,
    "provider": "anthropic",
    "api_key": "",
    "model": "claude-sonnet-4-6",
    "openai_model": "gpt-5.5",
    "max_tokens": 300,
    "timeout_seconds": 12,
}


class LLMConnector:
    """
    Optional, opt-in connector to a real LLM - Anthropic's Claude or
    OpenAI's GPT, selected via the 'provider' field in the config file -
    for handling messages that fall outside the chatbot's fixed
    rule-based/NN vocabulary. See the Section 6I module docstring above
    for the full design rationale and the fail-closed guarantee.

    Both providers are called directly over HTTPS with Python's
    built-in urllib (no anthropic/openai SDK needed), normalized behind
    the same generate_reply() interface so the rest of the bot doesn't
    need to know which provider is active.
    """

    ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
    ANTHROPIC_API_VERSION = "2023-06-01"
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    MAX_HISTORY_TURNS = 6  # user+assistant pairs kept for context

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_or_create_config()
        self.history = []  # list of {"role": ..., "content": ...} dicts
        self.last_error = None

    # ---- config -------------------------------------------------------

    def _load_or_create_config(self):
        if not os.path.exists(self.config_path):
            try:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(LLM_CONFIG_TEMPLATE, f, indent=2, ensure_ascii=False)
            except OSError:
                pass
            return dict(LLM_CONFIG_TEMPLATE)

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = dict(LLM_CONFIG_TEMPLATE)
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError):
            return dict(LLM_CONFIG_TEMPLATE)

    def provider(self) -> str:
        p = self.config.get("provider", "anthropic")
        return p if p in ("anthropic", "openai") else "anthropic"

    def set_provider(self, new_provider: str) -> dict:
        """
        Switches the active provider (anthropic/openai) and persists
        the choice back to the config file, so it survives a restart -
        this is what powers the in-chat 'change to gpt'/'change to
        claude' commands instead of requiring a manual file edit.

        Returns a dict describing what happened: {"switched": bool,
        "provider": str, "has_key": bool} - has_key tells the caller
        whether THIS provider already has a usable-looking key saved,
        since switching can't conjure a key that was never entered.
        Clears conversation history on an actual switch, since context
        from one model's conversation isn't meaningful to hand to a
        different provider's model.
        """
        new_provider = new_provider.strip().lower()
        if new_provider not in ("anthropic", "openai"):
            return {"switched": False, "provider": self.provider(), "has_key": self.is_available()}

        already_active = new_provider == self.provider()
        self.config["provider"] = new_provider
        self._save_config()
        if not already_active:
            self.clear_history()

        return {
            "switched": not already_active,
            "provider": new_provider,
            "has_key": self.is_available(),
        }

    def _save_config(self):
        """Persists the current in-memory config back to disk, so
        changes made via set_provider() survive a restart."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"[warning] could not save LLM config: {e}")

    def is_available(self) -> bool:
        """
        True only if the user has explicitly enabled this AND supplied
        something that looks like a real key FOR THE SELECTED PROVIDER.
        Does NOT guarantee the key is valid or the network is reachable -
        just that it's worth attempting a call.
        """
        if not self.config.get("enabled"):
            return False
        key = self.config.get("api_key", "")
        if not isinstance(key, str) or len(key) < 20:
            return False
        if self.provider() == "anthropic":
            return key.startswith("sk-ant-")
        else:  # openai
            # OpenAI keys start with "sk-", but so do Anthropic keys
            # ("sk-ant-...") - explicitly exclude that shape so an
            # Anthropic key left in the config doesn't get mistaken for
            # a usable OpenAI one (this caused a real false positive in
            # testing: switching providers reported success even though
            # no OpenAI key had actually been entered).
            return key.startswith("sk-") and not key.startswith("sk-ant-")

    def reload_config(self):
        """Re-reads the config file from disk, so the user can flip
        'enabled', switch providers, or update their key without
        restarting the bot."""
        self.config = self._load_or_create_config()

    # ---- conversation history ----------------------------------------

    def add_to_history(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        max_messages = self.MAX_HISTORY_TURNS * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]

    def clear_history(self):
        self.history = []

    # ---- the actual API call -------------------------------------------

    def generate_reply(self, user_text: str, system_prompt: str = None):
        """
        Sends user_text (plus recent history) to the configured LLM
        (whichever provider is selected) and returns its reply as a
        string, or None on ANY failure. Callers must always have an
        offline fallback ready - see the fail-closed guarantee in the
        Section 6I module docstring.
        """
        self.last_error = None
        if not self.is_available():
            self.last_error = "not configured or disabled"
            return None

        try:
            if self.provider() == "anthropic":
                reply_text = self._call_anthropic(user_text, system_prompt)
            else:
                reply_text = self._call_openai(user_text, system_prompt)
        except urllib.error.HTTPError as e:
            # Covers bad key (401), rate limits (429), bad request
            # (400), server errors (5xx) - all treated the same way:
            # fail closed and let the offline fallback take over.
            self.last_error = f"API returned HTTP {e.code}"
            print(f"[llm] {self.last_error}: falling back to offline mode")
            return None
        except urllib.error.URLError as e:
            self.last_error = f"couldn't reach the API ({e.reason})"
            print(f"[llm] {self.last_error}: falling back to offline mode")
            return None
        except TimeoutError:
            self.last_error = "request timed out"
            print(f"[llm] {self.last_error}: falling back to offline mode")
            return None
        except (json.JSONDecodeError, KeyError, ValueError, OSError) as e:
            self.last_error = f"unexpected error ({e})"
            print(f"[llm] {self.last_error}: falling back to offline mode")
            return None

        if reply_text is None:
            self.last_error = "unexpected response shape from API"
            return None

        self.add_to_history("user", user_text)
        self.add_to_history("assistant", reply_text)
        return reply_text

    def _call_anthropic(self, user_text: str, system_prompt: str):
        """Builds and sends an Anthropic Messages API request. Letting
        exceptions propagate to generate_reply()'s shared error handling
        rather than catching them here keeps both providers' failure
        modes handled identically in one place."""
        messages = list(self.history) + [{"role": "user", "content": user_text}]
        payload = {
            "model": self.config.get("model", "claude-sonnet-4-6"),
            "max_tokens": self.config.get("max_tokens", 300),
            "messages": messages,
        }
        if system_prompt:
            payload["system"] = system_prompt

        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.ANTHROPIC_API_URL,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.config["api_key"],
                "anthropic-version": self.ANTHROPIC_API_VERSION,
            },
        )
        timeout = self.config.get("timeout_seconds", 12)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_data = json.loads(response.read().decode("utf-8"))
        return self._extract_anthropic_text(response_data)

    def _call_openai(self, user_text: str, system_prompt: str):
        """Builds and sends an OpenAI Chat Completions API request -
        the same well-established endpoint format used by countless
        OpenAI-compatible providers, picked specifically because it
        needs no SDK, just a POST with a bearer token."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_text})

        payload = {
            "model": self.config.get("openai_model", "gpt-5.5"),
            "max_tokens": self.config.get("max_tokens", 300),
            "messages": messages,
        }

        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.OPENAI_API_URL,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['api_key']}",
            },
        )
        timeout = self.config.get("timeout_seconds", 12)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response_data = json.loads(response.read().decode("utf-8"))
        return self._extract_openai_text(response_data)

    @staticmethod
    def _extract_anthropic_text(response_data):
        """Pulls the text out of an Anthropic Messages API response,
        defensively - returns None if the shape isn't what's expected
        rather than raising, since a malformed/unexpected response
        should fail closed just like a network error would."""
        try:
            content_blocks = response_data.get("content", [])
            text_parts = [
                block.get("text", "")
                for block in content_blocks
                if isinstance(block, dict) and block.get("type") == "text"
            ]
            combined = "".join(text_parts).strip()
            return combined if combined else None
        except (AttributeError, TypeError):
            return None

    @staticmethod
    def _extract_openai_text(response_data):
        """Pulls the text out of an OpenAI Chat Completions response,
        defensively, same fail-closed philosophy as the Anthropic
        extractor above."""
        try:
            choices = response_data.get("choices", [])
            if not choices:
                return None
            message = choices[0].get("message", {})
            text = message.get("content", "")
            text = text.strip() if isinstance(text, str) else ""
            return text if text else None
        except (AttributeError, TypeError, IndexError):
            return None

    # ---- retry with backoff --------------------------------------------

    def generate_reply_with_retry(self, user_text: str, system_prompt: str = None,
                                    max_attempts: int = 3, base_delay: float = 0.75):
        """
        Same contract as generate_reply() (returns a string or None,
        never raises), but retries transient failures - timeouts and
        HTTP 429/5xx - with exponential backoff plus a little jitter,
        so a single dropped packet or a momentary rate limit doesn't
        take down the whole fallback path. Non-transient failures (bad
        key, disabled, malformed config) are NOT retried, since retrying
        those would just burn time for the exact same failure each time.
        """
        transient_markers = ("timed out", "HTTP 429", "HTTP 500", "HTTP 502",
                              "HTTP 503", "HTTP 504", "couldn't reach the API")
        last_reply = None
        for attempt in range(1, max_attempts + 1):
            last_reply = self.generate_reply(user_text, system_prompt)
            if last_reply is not None:
                return last_reply
            if not self.last_error or not any(marker in self.last_error for marker in transient_markers):
                return None  # non-transient - no point retrying
            if attempt < max_attempts:
                delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.25)
                time.sleep(delay)
        return last_reply

    # ---- token estimation ------------------------------------------------

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        A rough, offline token-count estimate - no tokenizer library
        needed. Uses the commonly-cited rule of thumb for English text
        (~4 characters per token), blended with a word-count-based
        estimate (~0.75 tokens per word) and averaged, since either
        heuristic alone drifts more on short or punctuation-heavy text
        than the two combined. This is an ESTIMATE for budgeting
        max_tokens/cost awareness, not an exact count - only the real
        provider-side tokenizer knows the true number.
        """
        if not text:
            return 0
        char_estimate = len(text) / 4.0
        word_count = len(text.split())
        word_estimate = word_count / 0.75
        return max(1, round((char_estimate + word_estimate) / 2))

    def estimate_cost_usd(self, text: str, rate_per_1k_tokens: float = 0.003) -> float:
        """Rough, offline cost estimate for a single call, using a
        caller-supplied rate (check current provider pricing - this
        file never hardcodes prices, since they change over time)."""
        tokens = self.estimate_tokens(text)
        return round((tokens / 1000.0) * rate_per_1k_tokens, 5)

    # ---- streaming-style chunked delivery ---------------------------------

    def stream_reply(self, user_text: str, system_prompt: str = None, chunk_size: int = 12):
        """
        Not real network streaming (the underlying providers' streaming
        endpoints use server-sent events, which would need a persistent
        connection this urllib-based client doesn't hold open) - this
        is a GENERATOR that yields the already-complete reply back to
        the caller in small word chunks, one at a time, so a GUI or CLI
        can print it progressively the way a real streaming reply feels,
        without actually needing the streaming API. Yields nothing (and
        the caller sees an empty generator) if generate_reply() itself
        returns None, so callers should treat "no chunks at all" as a
        failure signal the same way they'd treat a None return.
        """
        full_reply = self.generate_reply(user_text, system_prompt)
        if full_reply is None:
            return
        words = full_reply.split(" ")
        for i in range(0, len(words), chunk_size):
            yield " ".join(words[i:i + chunk_size])

    # ---- conversation summarization --------------------------------------

    def summarize_conversation(self, transcript_lines) -> str:
        """
        Asks the configured LLM to produce a short summary of a
        conversation transcript (list of "role: text" strings). Uses a
        dedicated, narrowly-scoped system prompt (PROMPT_TEMPLATES
        below) rather than the bot's general persona, since a summary
        request needs the model to STOP being conversational and just
        report facts. Returns None on any failure, same fail-closed
        contract as generate_reply() - callers should fall back to
        ExtractiveSummarizer (Section 6F/6J) when this returns None.
        """
        if not transcript_lines:
            return None
        joined = "\n".join(transcript_lines[-40:])  # cap length sent
        prompt = PROMPT_TEMPLATES["summarize_conversation"]["user_template"].format(transcript=joined)
        return self.generate_reply(prompt, system_prompt=PROMPT_TEMPLATES["summarize_conversation"]["system"])

    def apply_persona(self, persona_key: str, user_text: str):
        """
        Convenience wrapper: generate a reply using one of the named
        personas in PROMPT_TEMPLATES (see below) as the system prompt,
        rather than the caller having to remember/construct the exact
        prompt text each time. Falls back to no system prompt (plain
        generate_reply) if persona_key isn't recognized, rather than
        failing outright - an unrecognized persona shouldn't block a
        reply the model could otherwise give.
        """
        template = PROMPT_TEMPLATES.get(persona_key)
        system_prompt = template["system"] if template else None
        return self.generate_reply(user_text, system_prompt=system_prompt)


# ---- prompt template library -------------------------------------------
#
# A small, hand-written library of system prompts / prompt templates for
# specific LLM-backed tasks, kept separate from ad-hoc inline strings so
# every LLM-facing prompt in the file lives in ONE place and can be
# audited or tuned without hunting through handler methods. Every entry
# is plain, static text - nothing here is itself generated.

PROMPT_TEMPLATES = {
    "default_persona": {
        "system": (
            "You are a concise, friendly assistant embedded inside a larger "
            "rule-based chatbot. You are only invoked as a last resort, for "
            "messages the bot's offline rules and classifiers couldn't "
            "handle, so keep replies short (2-4 sentences unless asked for "
            "more) and avoid repeating what a simple rule-based reply "
            "would already say."
        ),
    },
    "summarize_conversation": {
        "system": (
            "You summarize chat transcripts. Output 3-5 short bullet points "
            "covering what was discussed and any decisions or facts the "
            "user shared (like their name or preferences). No preamble, no "
            "commentary, just the bullets."
        ),
        "user_template": "Summarize this conversation:\n\n{transcript}",
    },
    "explain_simply": {
        "system": (
            "Explain the user's question as simply as possible, the way "
            "you'd explain it to a curious teenager - short sentences, one "
            "concrete example, no jargon unless you immediately define it."
        ),
    },
    "creative_writer": {
        "system": (
            "You are a creative writing collaborator. Favor vivid, "
            "specific imagery over generic description, and keep whatever "
            "length the user implicitly asked for (a couplet stays a "
            "couplet; a story stays a story) rather than padding."
        ),
    },
    "code_helper": {
        "system": (
            "You help with small coding questions. Give a short, direct "
            "answer with a minimal code snippet if relevant, and mention "
            "one likely pitfall if there is an obvious one. Skip lengthy "
            "preambles."
        ),
    },
    "debate_partner": {
        "system": (
            "Present the strongest good-faith version of whichever side of "
            "an argument the user asks you to argue, clearly labeled as "
            "that side's case rather than your own settled opinion, and "
            "note the strongest counter-argument at the end."
        ),
    },
    "socratic_tutor": {
        "system": (
            "Instead of directly answering, ask ONE well-chosen guiding "
            "question that helps the user reach the answer themselves, "
            "unless they've explicitly asked you to just tell them."
        ),
    },
    "translator_polish": {
        "system": (
            "You polish already-translated text for natural phrasing in "
            "the target language, without changing its meaning. Point "
            "out, in one short note at the end, anything you weren't "
            "confident about (idioms, ambiguous pronouns) rather than "
            "silently guessing."
        ),
    },
    "empathetic_listener": {
        "system": (
            "The user may be venting or processing something difficult. "
            "Respond with brief, genuine acknowledgment before anything "
            "else - don't rush to solve, advise, or redirect unless "
            "they've asked for that."
        ),
    },
    "structured_data_extractor": {
        "system": (
            "Extract the requested fields from the user's text and "
            "respond with ONLY a JSON object containing those fields - "
            "no prose, no markdown fences. Use null for any field that "
            "isn't present in the text, rather than guessing a value."
        ),
    },
}


# ==============================================================================
# SECTION 6I-EXT: LLM RESPONSE CACHING (avoid redundant API calls)
# ==============================================================================
#
# A small in-memory cache keyed on (system_prompt, user_text), with a
# time-to-live so a repeated identical request within a session doesn't
# trigger a second network round-trip and a second charge against
# whatever usage budget the provider bills. This is the same idea as
# _RestApiClient's cache (Section 13) applied to the LLM path - LLM
# calls are the most latency- and cost-sensitive network calls this
# file makes, so caching them specifically is worth a dedicated class
# rather than folding it into the generic REST client.
class LLMResponseCache:
    def __init__(self, ttl_seconds: float = 600.0, max_entries: int = 200):
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._store = {}  # key -> (cached_at, response_text)
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _key(system_prompt, user_text) -> str:
        raw = f"{system_prompt or ''}\x01{user_text}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, system_prompt, user_text):
        key = self._key(system_prompt, user_text)
        entry = self._store.get(key)
        if entry is None:
            self.misses += 1
            return None
        cached_at, response_text = entry
        if time.time() - cached_at > self.ttl_seconds:
            del self._store[key]
            self.misses += 1
            return None
        self.hits += 1
        return response_text

    def set(self, system_prompt, user_text, response_text):
        if len(self._store) >= self.max_entries:
            # Evict the single oldest entry rather than clearing
            # everything - a cheap, if not perfectly LRU, eviction
            # policy appropriate for a cache this small.
            oldest_key = min(self._store, key=lambda k: self._store[k][0])
            del self._store[oldest_key]
        key = self._key(system_prompt, user_text)
        self._store[key] = (time.time(), response_text)

    def stats(self) -> str:
        total = self.hits + self.misses
        hit_rate = (self.hits / total) if total else 0.0
        return (f"LLM cache: {len(self._store)} entries, {self.hits} hits, "
                f"{self.misses} misses ({hit_rate:.0%} hit rate).")

    def clear(self):
        self._store = {}


# ==============================================================================
# SECTION 6I-EXT2: LLM USAGE/COST TRACKING (a running session budget)
# ==============================================================================
#
# Tracks cumulative ESTIMATED token usage and cost across a session
# (using LLMConnector.estimate_tokens/estimate_cost_usd, Section 6I),
# with an optional hard budget cap - once the estimated running total
# would exceed the cap, further LLM calls are refused BEFORE they'd be
# made, rather than after the fact. This is an estimate, not a bill:
# real provider-side tokenization differs slightly from the offline
# heuristic used here, so this is meant as a soft safety rail against
# runaway usage, not a precise accounting tool.
class LLMUsageTracker:
    def __init__(self, budget_usd: float = None, rate_per_1k_tokens: float = 0.003):
        self.budget_usd = budget_usd
        self.rate_per_1k_tokens = rate_per_1k_tokens
        self.total_prompt_tokens_est = 0
        self.total_completion_tokens_est = 0
        self.total_cost_est = 0.0
        self.call_count = 0

    def would_exceed_budget(self, prompt_text: str) -> bool:
        if self.budget_usd is None:
            return False
        prompt_tokens = LLMConnector.estimate_tokens(prompt_text)
        projected_cost = self.total_cost_est + (prompt_tokens / 1000.0) * self.rate_per_1k_tokens
        return projected_cost > self.budget_usd

    def record_call(self, prompt_text: str, completion_text: str):
        prompt_tokens = LLMConnector.estimate_tokens(prompt_text)
        completion_tokens = LLMConnector.estimate_tokens(completion_text or "")
        self.total_prompt_tokens_est += prompt_tokens
        self.total_completion_tokens_est += completion_tokens
        self.total_cost_est += ((prompt_tokens + completion_tokens) / 1000.0) * self.rate_per_1k_tokens
        self.call_count += 1

    def format_summary(self) -> str:
        lines = [
            f"LLM usage this session (estimated, not an exact bill):",
            f"  Calls made:          {self.call_count}",
            f"  Prompt tokens (est): {self.total_prompt_tokens_est:,}",
            f"  Completion tokens:   {self.total_completion_tokens_est:,}",
            f"  Estimated cost:      ${self.total_cost_est:.4f}",
        ]
        if self.budget_usd is not None:
            remaining = max(0.0, self.budget_usd - self.total_cost_est)
            lines.append(f"  Budget:              ${self.budget_usd:.2f} (${remaining:.4f} remaining)")
        return "\n".join(lines)


# ==============================================================================
# SECTION 6I-EXT3: PII SCRUBBER (privacy pre-check before any LLM call)
# ==============================================================================
#
# A lightweight, regex-based scanner that flags text that LOOKS LIKE it
# contains personal information - email addresses, phone numbers,
# credit-card-shaped digit sequences, and US-SSN-shaped digit sequences
# - before it would be sent to a third-party LLM API. This is NOT a
# content filter and never blocks anything; it's purely informational,
# giving the user a chance to reconsider before their message leaves
# the machine. Pattern-matching for "looks like an email/phone number/
# card number" is inherently approximate (it will both miss real PII
# in unusual formats and occasionally flag things that aren't actually
# sensitive) - it's a helpful nudge, not a guarantee.
class PIIScrubber:
    PATTERNS = {
        "email address": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
        "phone number": re.compile(r"\b(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b"),
        "credit-card-shaped number": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
        "US-SSN-shaped number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    }

    @classmethod
    def scan(cls, text: str) -> list:
        """Returns a list of the PII CATEGORY NAMES that matched (not
        the matched text itself, to avoid this scanner's own output
        becoming a place sensitive text gets echoed back)."""
        found = []
        for label, pattern in cls.PATTERNS.items():
            if pattern.search(text):
                found.append(label)
        return found

    @classmethod
    def warning_for(cls, text: str):
        """Returns a short warning string if `text` looks like it
        contains PII, or None if it looks clean."""
        found = cls.scan(text)
        if not found:
            return None
        joined = ", ".join(found)
        return (f"Heads up: this looks like it might contain a {joined}. "
                f"That's about to be sent to an external AI service - "
                f"want to remove it first?")


# ==============================================================================
# SECTION 6I-EXT4: CONVERSATION CONTEXT WINDOW (bounded multi-turn memory)
# ==============================================================================
#
# LLMConnector.generate_reply() (Section 6I) takes a single user_text
# and an optional system_prompt - genuinely useful for one-off
# requests (translation polishing, summarization, tool-calling), but
# multi-turn conversation benefits from the model seeing recent
# history too. This class builds that history into a single formatted
# block, kept under a token budget (using LLMConnector.estimate_tokens,
# Section 6I) by dropping the OLDEST turns first once the budget is
# exceeded - a standard, simple sliding-window context management
# strategy, appropriate for a small hobby bot (a production system
# would summarize dropped turns instead of just discarding them; this
# file keeps that possibility explicit rather than silently pretending
# discarded context is retained).
class ConversationContextWindow:
    def __init__(self, max_tokens: int = 800):
        self.max_tokens = max_tokens
        self.turns = []  # list of (speaker, text)

    def add_turn(self, speaker: str, text: str):
        self.turns.append((speaker, text))

    def clear(self):
        self.turns = []

    def build_context_block(self) -> str:
        """Returns the most recent turns, newest last, formatted as
        'speaker: text' lines, trimmed from the OLDEST end until the
        whole block fits within max_tokens (estimated)."""
        kept = list(self.turns)
        while kept:
            block = "\n".join(f"{speaker}: {text}" for speaker, text in kept)
            if LLMConnector.estimate_tokens(block) <= self.max_tokens:
                return block
            kept.pop(0)  # drop the oldest turn and try again
        return ""

    def build_prompt_with_context(self, new_user_text: str) -> str:
        context_block = self.build_context_block()
        if not context_block:
            return new_user_text
        return (f"Recent conversation so far:\n{context_block}\n\n"
                f"Now respond to this new message:\n{new_user_text}")


# ==============================================================================
# SECTION 6I-EXT5: RAG-STYLE CONTEXT (retrieval-augmented LLM prompts)
# ==============================================================================
#
# "RAG" (Retrieval-Augmented Generation) means retrieving relevant
# information from a knowledge source and folding it into the prompt
# BEFORE calling the model, so the model can ground its answer in that
# retrieved material instead of (or in addition to) whatever it
# already knows. Here, the "knowledge source" is the user's own
# remembered facts (MemoryStore, Section 2), and "retrieval" is real
# semantic search (SemanticMemoryIndex, Section 6H3 - torch contrastive
# embeddings when available, TF-IDF otherwise) rather than dumping
# every remembered fact into every prompt regardless of relevance.
#
# Previously, using remembered facts in an LLM call required an
# explicit "search my memory for X" command (Section 13's semantic_
# search intent). RAGContextBuilder makes that automatic: ANY LLM call
# routed through it first retrieves the top few facts relevant to the
# user's current message and prepends them as grounding context - the
# same underlying retrieval mechanism, just applied proactively rather
# than only on request.
class RAGContextBuilder:
    def __init__(self, semantic_memory: "SemanticMemoryIndex", memory_store: "MemoryStore",
                 top_k: int = 3, min_similarity: float = 0.15):
        self.semantic_memory = semantic_memory
        self.memory_store = memory_store
        self.top_k = top_k
        # Retrieved facts below this similarity score are dropped rather
        # than forced into the prompt - an irrelevant fact "grounding"
        # an unrelated question does more harm (confusing the model)
        # than leaving it out.
        self.min_similarity = min_similarity

    def retrieve(self, query: str):
        facts = self.memory_store.all_facts()
        if not facts:
            return []
        items = [f"{key.replace('_', ' ')}: {value}" for key, value in facts.items()]
        results = self.semantic_memory.search(query, items=items, top_k=self.top_k)
        return [(item, score) for item, score in results if score >= self.min_similarity]

    def build_augmented_prompt(self, user_text: str) -> str:
        """Returns user_text unchanged if nothing relevant was
        retrieved (so a RAG call with no useful context degrades
        gracefully to a plain call, not a prompt padded with
        boilerplate for nothing), or user_text prefixed with a
        grounding block of retrieved facts."""
        retrieved = self.retrieve(user_text)
        if not retrieved:
            return user_text
        facts_block = "\n".join(f"- {item}" for item, _score in retrieved)
        return (f"Relevant things you already know about this user:\n{facts_block}\n\n"
                f"User's message: {user_text}")

    def format_retrieval_preview(self, user_text: str) -> str:
        """A debugging/transparency helper - shows what WOULD be
        retrieved and injected for a given message, without actually
        calling the LLM. Useful for "why did it say that" style
        questions about RAG-augmented replies."""
        retrieved = self.retrieve(user_text)
        if not retrieved:
            return "Nothing in your remembered facts looked relevant enough to include."
        lines = ["Facts that would be retrieved for that message:"]
        for item, score in retrieved:
            lines.append(f"  - {item}  (relevance {score:.2f})")
        return "\n".join(lines)


class PromptBuilder:
    """
    Assembles few-shot prompts: a task instruction plus a handful of
    hand-written (input, output) example pairs, formatted consistently,
    so a caller doesn't have to hand-format examples inline every time.
    Pure string assembly - no model calls happen in this class; the
    caller passes the built prompt to LLMConnector.generate_reply().
    """

    def __init__(self, instruction: str):
        self.instruction = instruction
        self.examples = []  # list of (input_text, output_text)

    def add_example(self, input_text: str, output_text: str):
        self.examples.append((input_text, output_text))
        return self  # allow chaining: builder.add_example(...).add_example(...)

    def build(self, new_input: str) -> str:
        parts = [self.instruction.strip(), ""]
        for i, (ex_in, ex_out) in enumerate(self.examples, start=1):
            parts.append(f"Example {i}:")
            parts.append(f"Input: {ex_in}")
            parts.append(f"Output: {ex_out}")
            parts.append("")
        parts.append(f"Input: {new_input}")
        parts.append("Output:")
        return "\n".join(parts)

    def clear_examples(self):
        self.examples = []
        return self


class ExtractiveSummarizer:
    """
    Offline, non-LLM fallback for conversation/text summarization: ranks
    sentences by TF-IDF-weighted word overlap with the rest of the
    document (a classic, well-established extractive-summarization
    technique - essentially a tiny single-document version of the idea
    behind TextRank) and returns the top-N highest-scoring sentences, in
    their ORIGINAL order, so the summary still reads coherently rather
    than as a shuffled bag of high-scoring fragments.

    Used automatically by ChatBot whenever LLMConnector.summarize_
    conversation() returns None (LLM not configured, or a call failed),
    so summarization always has a working answer, just a less fluent
    one without the LLM.
    """

    def __init__(self):
        pass

    def is_llm_backed(self) -> bool:
        return False

    def summarize(self, text: str, max_sentences: int = 3) -> str:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        sentences = [s for s in sentences if len(s.split()) >= 3]
        if not sentences:
            return text.strip()
        if len(sentences) <= max_sentences:
            return " ".join(sentences)

        try:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf = vectorizer.fit_transform(sentences)
            scores = np.asarray(tfidf.sum(axis=1)).ravel()
        except ValueError:
            # Can happen on very short/degenerate input (e.g. all
            # stop words) - fall through to the word-frequency path.
            scores = self._word_frequency_scores(sentences)

        top_indices = sorted(np.argsort(scores)[-max_sentences:])
        return " ".join(sentences[i] for i in top_indices)

    @staticmethod
    def _word_frequency_scores(sentences):
        """Dependency-free fallback scorer, used only if TfidfVectorizer
        raises on degenerate input (e.g. every sentence is pure stop
        words): plain word-frequency sum per sentence, still a real
        extractive-ranking signal, just without TF-IDF's IDF weighting."""
        word_counts = Counter()
        for s in sentences:
            for w in re.findall(r"[a-zA-Z']+", s.lower()):
                word_counts[w] += 1
        scores = []
        for s in sentences:
            words = re.findall(r"[a-zA-Z']+", s.lower())
            scores.append(sum(word_counts[w] for w in words) / max(1, len(words)))
        return np.array(scores)


# ==============================================================================
