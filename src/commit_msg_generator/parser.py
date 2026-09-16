import re
from dataclasses import dataclass
from typing import List

@dataclass
class FileDiff:
    file: str
    status: str
    header: str
    hunk: str
    diff_content: str
    stats: tuple[str]


class DiffParser:
    def __init__(self, num_stat: str, name_status: str, diff_message: str) -> None:
        self.stat = num_stat
        self.status = name_status
        self.diff_msg = diff_message

    def get_stats(self):
        stats = []
        for line in self.stat.splitlines():
            added, deleted, filepath = line.split()
            stats.append(
                (int(added), int(deleted), str(filepath))
            )

    def get_status(self):
        name_status = []
        for line in self.status.splitlines():
            status, file = line.split()
            name_status.append(
                (status, file)
            )

    def get_diff_sections(self):
        diff_files = re.split(r'(?=diff)', self.diff_msg)
        for file in diff_files:
            header, hunk, content = re.split(r"(@@[^@]+@@\n)", file)


    def run(self) -> List[FileDiff]: