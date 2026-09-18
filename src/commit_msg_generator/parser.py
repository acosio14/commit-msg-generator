import re
from dataclasses import dataclass
from typing import List

@dataclass
class DiffContent:
    hunk: str
    content: str

@dataclass
class FileDiff:
    file: str
    status: str
    stats: tuple[str]
    header: str
    diffs: List[DiffContent]


class DiffParser:
    def __init__(self, num_stat_msg: str, name_status_msg: str, diff_message: str) -> None:
        self.stat = num_stat_msg
        self.status = name_status_msg
        self.diff_msg = diff_message


    def _get_stats(self):
        num_stats = {}
        for line in self.stat.splitlines():
            added, deleted, filepath = line.split()
            num_stats[filepath] = {}
            num_stats[filepath]["added"] = int(added)
            num_stats[filepath]["deleted"] = int(deleted)

        return num_stats


    def _get_status(self):
        name_status = {}
        for line in self.status.splitlines():
            status, file = line.split()
            name_status[file] = status

        return name_status


    def _get_diff_sections(self, file_section):
        diff_content_list = []
        for section in file_section:
            header, file_diff = re.split(r"(?=@@[\d\s\+\-\,]+@@)", section, maxsplit=1)

            diffs = re.split(r"(?=@@[\d\s\+\-\,]+@@)", file_diff)
            for diff in diffs:
                hunk, content = re.split(r"(?=@@[\d\s\+\-\,]+@@)", diff)
                diff_content_list.append(DiffContent(hunk, content))

        return header, diff_content_list


    def _extract_filename(self, file_section):
        # To-Do: Need to get filename parsed from here to go along with header, hunks, contents
        ...

    def run(self) -> List[FileDiff]:
        file_sections = re.split(r'(?=diff)', self.diff_msg)
        name_status_list = self._get_status() # status, file
        num_stats_list = self._get_stats() # added, deleted, filepath

        for file_section in file_sections:
            filename = self._extract_filename(file_section)
            # To-Do: Change status and stats to dicts then I can use key/value pairs to extract values from them and store in dataclass
            header, diff_content_list = self._get_diff_sections(file_section)

            FileDiff(filename, status, stats, header, diff_content_list)