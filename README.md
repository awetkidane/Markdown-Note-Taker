# Markdown Note Taker — Usage Guide

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app (from the project root)
python -m markdown_taker
```

The app scans the **current working directory** for `.md` files and presents them in a split-pane TUI.

---

## Layout

```
┌─ Header ──────────────────────────────────────────┐
├─ Sidebar (25%) ──── Editor (75%) ─────────────────┤
│  notes.md           [edit your markdown here]      │
│  todo.md                                           │
│  journal.md                                        │
├─ Ctrl+N:New  Tab:Focus  Ctrl+Q:Quit ──────────────┘
```

- **Left sidebar** — lists every `.md` file in the directory.
- **Right editor** — full-featured text area for editing the selected file.
- **Bottom footer** — shows available keyboard shortcuts and a **Saving...** indicator.

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `↑` / `↓` | Navigate the file list (sidebar focused) |
| `Enter` | Open the highlighted file in the editor |
| `Tab` | Move focus from sidebar → editor |
| `Shift+Tab` | Move focus from editor → sidebar |
| `Ctrl+N` | Create a new markdown file (opens a dialog) |
| `Ctrl+Q` or `Q` | Save current file and quit |

---

## Auto-Save

- Content is saved to disk **automatically** 1.5 seconds after you stop typing.
- A yellow **Saving...** indicator appears in the footer while the save is in progress.
- Files are also flushed to disk when you quit (`Ctrl+Q` / `Q`).

---

## Creating a New File

1. Press **`Ctrl+N`** — a modal dialog appears.
2. Type the file name (the `.md` extension is added automatically if omitted).
3. Press **Enter** to confirm, or **Escape** to cancel.
4. The new file is created, added to the sidebar, and loaded into the editor.

---

## Notes

- All files are relative to the directory where you ran `python -m markdown_taker`.
- If no `.md` files exist on startup, a blank `untitled.md` is created automatically.
- File read/write errors are reported via in-app notifications.
