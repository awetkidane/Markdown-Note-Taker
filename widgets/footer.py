from rich.text import Text
from textual.reactive import reactive
from textual.widget import Widget


class AppFooter(Widget):
    """One-line bar at the bottom showing essential shortcuts and the
    transient "Saving…" indicator."""

    saving = reactive(False)

    DEFAULT_CSS = """
    AppFooter {
        height: 1;
        dock: bottom;
        background: $panel;
        color: $text;
        padding: 0 1;
    }
    """

    def render(self) -> Text:
        result = Text(
            " Ctrl+N:New  Tab:Focus  Ctrl+Q:Quit",
            style="bold",
        )
        if self.saving:
            result.append("    ", style="")
            result.append("Saving...", style="italic yellow")
        return result
