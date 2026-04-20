from __future__ import annotations

from pathlib import Path
from typing import Sequence


def scan_files(
    paths: Sequence[Path],
    extension: str,
    recursive: bool = True,
) -> list[Path]:
    """Return all files matching *extension* found under *paths*.

    Directories are walked (recursively when *recursive* is True).
    Plain file paths are included directly if their extension matches.
    """
    ext = extension.lower()
    found: list[Path] = []

    for path in paths:
        if path.is_dir():
            pattern = f"**/*{ext}" if recursive else f"*{ext}"
            found.extend(sorted(path.glob(pattern)))
        elif path.is_file() and path.suffix.lower() == ext:
            found.append(path)

    return found
