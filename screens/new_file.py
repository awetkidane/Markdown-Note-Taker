from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Input, Label


class NewFileScreen(Screen):
    """Modal overlay that asks the user for a new file name.

    Dismisses with the entered name (or ``None`` when cancelled).
    """

    DEFAULT_CSS = """
    NewFileScreen {
        align: center middle;
    }

    NewFileScreen #dialog {
        width: 50;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    NewFileScreen Label {
        margin-bottom: 1;
        text-style: bold;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    def compose(self):
        with Vertical(id="dialog"):
            yield Label("Create New Markdown File")
            yield Input(placeholder="Enter file name (e.g., meeting-notes)")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)

    def action_cancel(self) -> None:
        self.dismiss(None)
