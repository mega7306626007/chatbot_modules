"""Kivy graphical chat window, optional --gui (Section 11)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 11: KIVY GRAPHICAL CHAT WINDOW (optional, --gui)
# ==============================================================================
#
# A graphical alternative to the plain-text CLI loop above, built with
# Kivy - chosen specifically because it's one of the standard ways to
# get a real touch-friendly GUI running under Pydroid 3 on Android,
# with `pip install kivy` (or Pydroid 3's own package manager) being
# the only extra step beyond what this file already needs.
#
# This section is ENTIRELY OPTIONAL and additive:
#   - If Kivy isn't installed, KIVY_AVAILABLE is False (see the import
#     block near the top of the file) and none of the classes below
#     get defined - the rest of the file (CLI loop, --test mode) is
#     completely unaffected.
#   - The GUI talks to the exact same ChatBot class as the CLI loop -
#     same respond(), same memory, same database, same neural
#     networks - so nothing about the chatbot's actual behavior changes
#     based on which interface you're using.
#
# Layout: a scrollable message log (each turn as a left/right-ish
# aligned label, oldest at top, auto-scrolling to the bottom on new
# messages), a text input + Send button row, and a row of shortcut
# buttons (Help / Stats / LLM Status) that just inject the
# corresponding command and send it - useful on a touchscreen where
# typing "nn stats" character by character is more friction than
# tapping a button.

if KIVY_AVAILABLE:

    class ChatBubble(Label):
        """
        A single chat message rendered as a wrapping, auto-sizing
        Label. Kivy's Label doesn't automatically grow its height to
        fit wrapped text, so this binds text_size to the available
        width and height back to the resulting texture size - the
        standard pattern for a chat-log-style label in Kivy.
        """

        def __init__(self, text: str, is_user: bool, **kwargs):
            super().__init__(
                text=text,
                size_hint_y=None,
                halign="right" if is_user else "left",
                valign="middle",
                color=(0.85, 0.92, 1, 1) if is_user else (1, 1, 1, 1),
                **kwargs,
            )
            self.bind(width=self._update_text_size)
            self.bind(texture_size=self._update_height)

        def _update_text_size(self, instance, width):
            self.text_size = (width, None)

        def _update_height(self, instance, texture_size):
            self.height = texture_size[1] + dp(12)

    class ChatBotApp(App):
        """
        The Kivy application itself. Owns one ChatBot instance for the
        lifetime of the app (created in build(), saved/flushed in
        on_stop()) - the same lifecycle the CLI's run_chat_loop()
        follows, just driven by GUI events instead of a blocking input()
        loop.
        """

        title = "PyChat"

        def build(self):
            self.bot = ChatBot()
            Window.clearcolor = (0.10, 0.10, 0.12, 1)

            root = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(6))

            # --- scrollable message log ---
            self.message_grid = GridLayout(
                cols=1, size_hint_y=None, spacing=dp(6), padding=(dp(4), dp(4))
            )
            self.message_grid.bind(minimum_height=self.message_grid.setter("height"))

            self.scroll = ScrollView(size_hint=(1, 1), bar_width=dp(6))
            self.scroll.add_widget(self.message_grid)
            root.add_widget(self.scroll)

            # --- shortcut buttons row ---
            shortcuts = BoxLayout(orientation="horizontal", size_hint_y=None,
                                   height=dp(40), spacing=dp(6))
            for label_text, command in [
                ("Help", "help"),
                ("Stats", "show stats"),
                ("NN Stats", "nn stats"),
                ("LLM Status", "llm status"),
                ("System", "system status"),
            ]:
                btn = Button(text=label_text)
                btn.bind(on_release=lambda _btn, cmd=command: self._send_text(cmd))
                shortcuts.add_widget(btn)
            root.add_widget(shortcuts)

            # --- text input + send row ---
            input_row = BoxLayout(orientation="horizontal", size_hint_y=None,
                                   height=dp(48), spacing=dp(6))
            self.text_input = TextInput(
                multiline=False, hint_text="Type a message...",
                size_hint_x=0.8,
            )
            self.text_input.bind(on_text_validate=lambda _w: self._on_send())
            send_btn = Button(text="Send", size_hint_x=0.2)
            send_btn.bind(on_release=lambda _w: self._on_send())
            input_row.add_widget(self.text_input)
            input_row.add_widget(send_btn)
            root.add_widget(input_row)

            # Greet the user the same way the CLI banner does, so the
            # GUI isn't a silent blank screen on first launch.
            Clock.schedule_once(lambda _dt: self._show_greeting(), 0)

            return root

        def _show_greeting(self):
            name = self.bot.bot_name()
            visit_count = self.bot.memory.get_visit_count()
            if visit_count > 1:
                greeting = f"Welcome back! This is visit #{visit_count}. I'm {name}."
            else:
                greeting = f"Hi! I'm {name}, your chatbot. Type 'help' to see what I can do."
            self._add_bubble(greeting, is_user=False)

        def _on_send(self):
            text = self.text_input.text.strip()
            if not text:
                return
            self.text_input.text = ""
            self._send_text(text)

        def _send_text(self, text: str):
            """Shared path for both typed messages and shortcut-button
            taps - logs the turn, calls the SAME ChatBot.respond() the
            CLI uses, and renders both sides of the exchange."""
            self._add_bubble(text, is_user=True)
            self.bot.logger.log("user", text)
            reply = self.bot.respond(text)
            self.bot.logger.log("bot", reply)
            self._add_bubble(reply, is_user=False)

        def _add_bubble(self, text: str, is_user: bool):
            prefix = "You: " if is_user else f"{self.bot.bot_name()}: "
            bubble = ChatBubble(prefix + text, is_user=is_user)
            self.message_grid.add_widget(bubble)
            # Auto-scroll to the newest message on the next frame, once
            # layout has actually happened and scroll_y is meaningful.
            Clock.schedule_once(lambda _dt: setattr(self.scroll, "scroll_y", 0), 0)

        def on_stop(self):
            """Mirrors run_chat_loop()'s finally block - make sure
            memory and the conversation log are flushed even when the
            app is closed via the window controls rather than a chat
            command."""
            self.bot.memory.save()
            self.bot.logger.flush_to_disk()


def run_gui():
    """Entry point for `python chatbot.py --gui`. Prints a clear,
    actionable message instead of a raw ModuleNotFoundError if Kivy
    isn't installed, since that's a much more useful failure for
    someone running this on Pydroid 3 for the first time."""
    if not KIVY_AVAILABLE:
        print(
            "The graphical interface needs Kivy, which isn't installed.\n"
            "On Pydroid 3: open the Pip menu and install 'kivy' (or run "
            "'pip install kivy' from a terminal), then try --gui again.\n"
            "Everything else in this file still works without it - run "
            "without --gui for the plain-text chat, or --test for the self-test."
        )
        return
    ChatBotApp().run()


# ==============================================================================
