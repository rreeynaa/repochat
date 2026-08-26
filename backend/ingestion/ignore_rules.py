"""
Determines which files/directories should NOT be indexed.

Combines a set of sensible built-in defaults with an optional per-repository
`.codeignore` file (same syntax as .gitignore: one glob pattern per line,
'#' starts a comment, blank lines are skipped).
"""

import fnmatch
from pathlib import Path

# Directories we never want to walk into, regardless of .codeignore.
DEFAULT_IGNORED_DIRS = {
    ".git", "node_modules", "venv", ".venv", "env", "__pycache__",
    "build", "dist", "out", "target", ".idea", ".vscode",
    ".mypy_cache", ".pytest_cache", ".tox", "coverage",
    ".next", ".nuxt", "vendor", "bin", "obj",
}

# File extensions we never want to index (binaries, media, archives, etc.)
DEFAULT_IGNORED_EXTENSIONS = {
    # images
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".webp",
    # video / audio
    ".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav", ".flac",
    # archives
    ".zip", ".tar", ".gz", ".rar", ".7z",
    # compiled / binary
    ".pyc", ".pyo", ".class", ".o", ".so", ".dll", ".exe", ".bin",
    ".woff", ".woff2", ".ttf", ".eot",
    # data blobs / lockfiles that are huge and not useful to chunk semantically
    ".lock", ".log",
}

# If a file is bigger than this, skip it (protects RAM + avoids indexing
# generated/minified files or datasets that got committed by accident).
DEFAULT_MAX_FILE_SIZE_BYTES = 1_000_000  # 1 MB

# Filenames that are almost always generated/vendored, even without a
# recognizable "ignored" extension.
DEFAULT_IGNORED_FILENAMES = {
    "package-lock.json", "yarn.lock", "poetry.lock", "Pipfile.lock",
    "Cargo.lock", ".DS_Store",
}


class IgnoreRules:
    def __init__(self, repo_root: Path, extra_patterns: list[str] | None = None):
        self.repo_root = repo_root
        self.patterns: list[str] = list(extra_patterns or [])
        self._load_codeignore_file()

    def _load_codeignore_file(self) -> None:
        codeignore_path = self.repo_root / ".codeignore"
        if not codeignore_path.exists():
            return
        with open(codeignore_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                self.patterns.append(line)

    def is_dir_ignored(self, dir_name: str) -> bool:
        if dir_name in DEFAULT_IGNORED_DIRS:
            return True
        if dir_name.startswith("."):
            # Hidden directories: ignore by default (matches .git, .venv, etc.
            # that aren't already caught above).
            return True
        return any(fnmatch.fnmatch(dir_name, pat) for pat in self.patterns)

    def is_file_ignored(self, file_path: Path) -> bool:
        name = file_path.name
        if name in DEFAULT_IGNORED_FILENAMES:
            return True
        if file_path.suffix.lower() in DEFAULT_IGNORED_EXTENSIONS:
            return True
        try:
            if file_path.stat().st_size > DEFAULT_MAX_FILE_SIZE_BYTES:
                return True
        except OSError:
            return True
        rel_str = str(file_path.relative_to(self.repo_root))
        return any(
            fnmatch.fnmatch(rel_str, pat) or fnmatch.fnmatch(name, pat)
            for pat in self.patterns
        )
