from pathlib import Path
from typing import List

from textual.binding import Binding
from textual.widgets import Label, ListItem, ListView


class FileSidebar(ListView):
    """Left-side file list that shows every ``.md`` file in the CWD.

    Sends a ``ListView.Selected`` message (inherited) when the user
    presses Enter on an item.  Bind **[Tab]** to jump into the editor.
    """

    BINDINGS = [
        Binding("tab", "focus_editor", "Focus Editor", show=False),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._files: List[Path] = []

    def populate(self, files: List[Path]) -> None:
        """Replace the current list with *files*."""
        self._files = files
        self.clear()
        for path in files:
            self.append(ListItem(Label(path.name)))

    def action_focus_editor(self) -> None:
        """Move keyboard focus to the right-hand editor pane."""
        self.screen.query_one("#editor").focus()
