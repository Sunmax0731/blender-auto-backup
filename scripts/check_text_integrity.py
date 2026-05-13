from __future__ import annotations

from pathlib import Path
import string

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".toml", ".txt", ".yml", ".yaml", ".js"}
SKIP_DIRS = {".git", "dist", "__pycache__", ".pytest_cache", "node_modules"}
MOJIBAKE_MARKERS = tuple(chr(codepoint) for codepoint in (0x7E3A, 0x7E67, 0x9B2F, 0x90E2, 0xFFFD))
ALLOWED_CONTROLS = {"\n", "\r", "\t"}


def iter_text_files():
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> None:
    failures: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                failures.append(f"{path.relative_to(ROOT)} contains mojibake marker {marker}")
        for index, char in enumerate(text):
            if char in ALLOWED_CONTROLS:
                continue
            if ord(char) < 32:
                name = string.printable[ord(char)] if ord(char) < len(string.printable) else str(ord(char))
                failures.append(f"{path.relative_to(ROOT)} contains control character {name} at {index}")
                break
    if failures:
        raise SystemExit("\n".join(failures))
    print("text integrity check passed")


if __name__ == "__main__":
    main()
