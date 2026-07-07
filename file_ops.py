from pathlib import Path
from typing import List


def discover_markdown_files(directory: str = ".") -> List[Path]:
    """Return all .md files in *directory*, sorted alphabetically."""
    return sorted(Path(directory).glob("*.md"))


def ensure_default_file(directory: str = ".") -> Path:
    """Create ``untitled.md`` when no markdown files exist yet."""
    path = Path(directory) / "untitled.md"
    path.write_text("", encoding="utf-8")
    return path


def read_file(path: Path) -> str:
    """Return the full text content of *path*."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except (OSError, PermissionError) as exc:
        raise RuntimeError(f"Cannot read {path.name}: {exc}") from exc


def write_file(path: Path, content: str) -> None:
    """Persist *content* to *path*."""
    try:
        path.write_text(content, encoding="utf-8")
    except (OSError, PermissionError) as exc:
        raise RuntimeError(f"Cannot write {path.name}: {exc}") from exc


def create_file(directory: str, name: str) -> Path:
    """Create a new .md file (appends ``.md`` suffix if missing)."""
    if not name.endswith(".md"):
        name += ".md"
    path = Path(directory) / name
    path.write_text("", encoding="utf-8")
    return path
