from dataclasses import dataclass

@dataclass
class ChunkMsg:
    file: str # Path
    start_line_num: int
    text: str

@dataclass
class GitDiffMsg:
    changes: list[ChunkMsg]
    raw_text: str
