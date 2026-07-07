import asyncio
from pathlib import Path

from textual.binding import Binding
from textual.message import Message
from textual.widgets import TextArea

from markdown_taker.file_ops import read_file, write_file


class EditorPane(TextArea):
    """Right-hand text editor with a 1.5 s debounced auto-save.

    Every keystroke restarts a 1.5 s timer.  When the timer fires the
    current content is written to disk.  A ``SaveStatusChanged`` message
    is posted so the footer can show a "Saving…" indicator.
    """

    class SaveStatusChanged(Message):
        """Posted when the saving state flips (on ⇒ off or off ⇒ on)."""
        def __init__(self, saving: bool) -> None:
            self.saving = saving
            super().__init__()

    BINDINGS = [
        Binding("shift+tab", "focus_sidebar", "Focus Sidebar", show=False),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_file: Path | None = None
        self._save_task: asyncio.Task | None = None
        self._loading: bool = False

    # ------------------------------------------------------------------
    # File loading
    # ------------------------------------------------------------------

    def load_file(self, path: Path) -> None:
        """Read *path* into the editor, cancelling any pending save."""
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
            self._save_task = None

        self.current_file = path
        self._loading = True
        try:
            self.text = read_file(path)
        finally:
            self._loading = False

    # ------------------------------------------------------------------
    # Debounced auto-save
    # ------------------------------------------------------------------

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Restart the auto-save timer on every edit.

        Ignored during :meth:`load_file` to avoid a spurious save of
        content that was just read from disk.
        """
        if self.current_file is None or self._loading:
            return
        self._debounce_save()

    def _debounce_save(self) -> None:
        """Cancel any outstanding save and schedule a fresh one."""
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
        self._save_task = asyncio.create_task(self._auto_save())

    async def _auto_save(self) -> None:
        """Wait 1.5 s of quiet, then persist content."""
        try:
            await asyncio.sleep(1.5)
        except asyncio.CancelledError:
            return

        fp = self.current_file
        if fp is None:
            return

        self.post_message(self.SaveStatusChanged(True))
        try:
            write_file(fp, self.text)
        except RuntimeError:
            self.notify("Save failed", severity="error")
        finally:
            self.post_message(self.SaveStatusChanged(False))
            self._save_task = None

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def action_focus_sidebar(self) -> None:
        """Move keyboard focus back to the sidebar."""
        self.screen.query_one("#sidebar").focus()
