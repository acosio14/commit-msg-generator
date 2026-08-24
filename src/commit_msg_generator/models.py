from dataclasses import dataclass
from enum import StrEnum


class FileStatus(StrEnum):
    """How a file changed, derived from git diff headers (no LLM required)."""
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    RENAMED = "renamed"
    COPIED = "copied"
    BINARY = "binary"


@dataclass
class ChunkMsg:
    file: str  # Path (new name for renames/copies)
    start_line_num: int
    text: str
    status: FileStatus

@dataclass
class GitDiffMsg:
    changes: list[ChunkMsg]
    raw_text: str
