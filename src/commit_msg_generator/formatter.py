import logging
from commit_msg_generator.parser import FileDiff
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Prompt:
    msg: str

# To-Do: 
# - Add conditional that if status is renamed, create separate renamed formatter with less context
# - Maybe add functionality that deals with large diffs (truncate, summarize, other?)
def format_file_diffs(list_file_diffs: FileDiff) -> Prompt:
    formatted_diffs = []
    for file_diffs in list_file_diffs:
        diff_header = (
            f"<file> {file_diffs.file}</file>\n"
            f"<status>{file_diffs.status}</status\n"
            f"<stats>{file_diffs.stats}</stats>\n"
            f"<header>{file_diffs.header}</header>\n"
        )
        diffs = ""
        for diff in file_diffs:
            diff = (
                "<diffs>\n"
                f"<hunk>{diff.hunk}</hunk>j\n"
                f"<content>{diff.cotent}</content>\n"
                "</diffs>\n"
            )
            diffs += diff

        formatted_diffs.append(diff_header + diffs)

    return Prompt(
        "Using the information of the git diff in the " \
        "delimited triple backticks in xml format, " \
        "write 3 conventional commit messages.\n" \
        f"```\n {("").join(formatted_diffs)}\n```"
    )
    
