from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Header, ListView

from markdown_taker.file_ops import (
    create_file,
    discover_markdown_files,
    ensure_default_file,
    write_file,
)
from markdown_taker.screens.new_file import NewFileScreen
from markdown_taker.widgets.editor import EditorPane
from markdown_taker.widgets.footer import AppFooter
from markdown_taker.widgets.sidebar import FileSidebar


class MarkdownApp(App):
    """Markdown Note Taker — a lightweight split-pane TUI editor.

    Layout
    ------
    ┌─ Header ─────────────────────────────────┐
    ├─ Sidebar (25 %) ── Editor (75 %) ────────┤
    │  file-1.md        [editable content]      │
    │  file-2.md                                │
    ├─ Footer (shortcuts + "Saving…") ─────────┘
    """

    DEFAULT_CSS = """
    Screen {
        layout: vertical;
    }

    #main-layout {
        height: 1fr;
        layout: horizontal;
    }

    #sidebar {
        width: 25%;
        min-width: 20;
        border: solid $primary;
    }

    #editor {
        width: 75%;
        border: solid $secondary;
    }
    """

    BINDINGS = [
        Binding("ctrl+n", "new_file", "New File"),
        Binding("ctrl+q", "exit_app", "Quit"),
        Binding("q", "exit_app", "Quit"),
    ]

    # ------------------------------------------------------------------
    # Composition (layout initialisation)
    # ------------------------------------------------------------------

    def compose(self) -> ComposeResult:
        """Build the three-zone UI: header, split pane, status footer."""
        yield Header()
        with Horizontal(id="main-layout"):
            yield FileSidebar(id="sidebar")
            yield EditorPane(id="editor")
        yield AppFooter()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def on_mount(self) -> None:
        """Startup: scan for ``.md`` files, populate the sidebar and
        load the first (or a freshly-created default) file."""
        files = discover_markdown_files()

        if not files:
            try:
                default = ensure_default_file()
                files = [default]
            except (OSError, PermissionError) as exc:
                self.notify(str(exc), severity="error")
                return

        sidebar = self.query_one(FileSidebar)
        sidebar.populate(files)
        sidebar.index = 0

        # Focus the editor so the user can start typing immediately.
        editor = self.query_one(EditorPane)
        editor.load_file(files[0])
        editor.focus()

    # ------------------------------------------------------------------
    # Message handlers
    # ------------------------------------------------------------------

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """User pressed Enter on a file in the sidebar — load it."""
        sidebar = self.query_one(FileSidebar)
        if sidebar.index is not None and sidebar.index < len(sidebar._files):
            path = sidebar._files[sidebar.index]
            self.query_one(EditorPane).load_file(path)

    def on_editor_pane_save_status_changed(
        self, event: EditorPane.SaveStatusChanged
    ) -> None:
        """Toggle the "Saving…" indicator in the footer bar."""
        self.query_one(AppFooter).saving = event.saving

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def action_new_file(self) -> None:
        """Show a modal input, then create the file and focus the editor."""

        def _on_name(name: str | None) -> None:
            if not name or not name.strip():
                return
            name = name.strip()
            if not name.endswith(".md"):
                name += ".md"

            try:
                path = create_file(".", name)
            except (OSError, PermissionError) as exc:
                self.notify(str(exc), severity="error")
                return

            # Refresh sidebar and select the new entry.
            files = discover_markdown_files()
            sidebar = self.query_one(FileSidebar)
            sidebar.populate(files)
            try:
                sidebar.index = files.index(path)
            except ValueError:
                sidebar.index = 0

            editor = self.query_one(EditorPane)
            editor.load_file(path)
            editor.focus()

        self.push_screen(NewFileScreen(), _on_name)

    async def action_exit_app(self) -> None:
        """Flush any pending content to disk before quitting."""
        editor = self.query_one(EditorPane)
        if editor.current_file is not None:
            # Cancel a pending debounce and write immediately.
            if editor._save_task and not editor._save_task.done():
                editor._save_task.cancel()
                editor._save_task = None
            try:
                write_file(editor.current_file, editor.text)
            except RuntimeError:
                pass  # Best-effort on exit.
        self.exit()
