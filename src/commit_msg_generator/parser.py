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
    stats: dict[str,int]
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
        """
        A (Added): A brand new file was created and added to the repository.
        M (Modified): The contents or the file permissions (mode) of an existing file have changed.
        D (Deleted): An existing file has been deleted from the project.
        R (Renamed): The file was renamed or moved to a different folder path.
        C (Copied): A file was copied into a completely new file.
        T (Type Changed): The type of the file changed (for example, a regular file was turned into a symbolic link or a submodule).
        U (Unmerged): The file has unresolved merge conflicts. You must fix the conflicts before committing.
        B (Pairing Broken): The file was heavily modified, making Git break the connection between the old version and the new version.
        X (Unknown): An unknown change type occurred (usually indicates an internal Git bug)
        """
        status_type = {
            "A" : "Added",
            "M" : "Modified",
            "D" : "Deleted",
            "R" : "Renamed",
            "C" : "Copied",
            "T" : "Type Changed",
            "U" : "Unmerged",
            "B" : "Pairing Broken",
            "X" : "Unknown"
        }
        name_status = {}
        for line in self.status.splitlines():
            output_status, file = line.split()
            status = status_type.get(output_status[0])
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


    def _extract_filename(self, file_section: str):
        top_diff_header = file_section.splitlines()[0]
        return re.split(r'?<=b/', top_diff_header)[0]
        


    def run(self) -> List[FileDiff]:
        file_sections = re.split(r'(?=diff\s--git)', self.diff_msg)
        name_status = self._get_status() # status, file
        num_stats = self._get_stats() # added, deleted, filepath

        file_diff_list = []
        for file_section in file_sections:
            filename = self._extract_filename(file_section)
            status = name_status.get(filename)
            stats = num_stats.get(filename)
            header, diff_content_list = self._get_diff_sections(file_section)

            file_diff_list.append(FileDiff(filename, status, stats, header, diff_content_list))

        return file_diff_list