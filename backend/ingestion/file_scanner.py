"""
Walks a repository directory tree and returns the list of files that should
be indexed, respecting DEFAULT_IGNORED_DIRS/EXTENSIONS and any .codeignore.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from backend.ingestion.ignore_rules import IgnoreRules

# Maps file extension -> a language label used throughout the system
# (metadata, UI filters, language detection).
EXTENSION_TO_LANGUAGE = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".hpp": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".sql": "sql",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
}

SUPPORTED_EXTENSIONS = set(EXTENSION_TO_LANGUAGE.keys())


@dataclass
class ScannedFile:
    absolute_path: Path
    relative_path: str  # relative to repo root, uses forward slashes
    language: str


def scan_repository(repo_root: str | Path, extra_ignore_patterns: list[str] | None = None) -> list[ScannedFile]:
    """
    Recursively scans repo_root and returns every file we know how to
    process, skipping ignored directories/files as it goes (so we never
    even descend into e.g. node_modules).
    """
    repo_root = Path(repo_root).resolve()
    if not repo_root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_root}")
    if not repo_root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {repo_root}")

    ignore_rules = IgnoreRules(repo_root, extra_ignore_patterns)
    results: list[ScannedFile] = []

    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Prune ignored directories in-place so os.walk doesn't descend into them.
        dirnames[:] = [d for d in dirnames if not ignore_rules.is_dir_ignored(d)]

        for filename in filenames:
            file_path = Path(dirpath) / filename
            extension = file_path.suffix.lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue
            if ignore_rules.is_file_ignored(file_path):
                continue

            relative_path = file_path.relative_to(repo_root).as_posix()
            results.append(
                ScannedFile(
                    absolute_path=file_path,
                    relative_path=relative_path,
                    language=EXTENSION_TO_LANGUAGE[extension],
                )
            )

    return results
