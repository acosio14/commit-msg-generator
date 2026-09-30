import logging
from commit_msg_generator.parser import FileDiff
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Prompt:
    msg: str

# from parser:
# [ FileDiff(filename, status, stats, header, [ DiffContent(hunk, content) ]) ]
"""
FileDiff(
    "src/example.py",
    "Modified",
    {
        "added_lines": 1,
        "deleted_lines": 1
    },
    "diff --git a/src/example.py b/src/example.py\nindex f063189..a2dd04a 100644\n--- a/src/example.py\n+++ b/src/example.py\n",
    [
        DiffContent(
            "@@ -91,4 +91 @@",
            " class Addition:\n- a = 10\n+ a = 11"
        )
    ]
)
"""


# To-Do: Add conditional that if status is rename, create separate prompt (retriever func)
def format_file_diffs(list_file_diffs: FileDiff) -> Prompt:
    formatted_diffs = []
    for file_diffs in list_file_diffs:
        diff_header = (
            f"<file> {file_diffs.file}</file>\n"
            f"<status>{file_diffs.status}</status\n"
            f"<stats>{file_diffs.stats}</stats>\n"
        )
        diffs = ""
        for diff in file_diffs:
            # To-Do: append to this so it can be a section of multiple chunks
            diff = (
                "<diffs>\n"
                f"<hunk>{diff.hunk}</hunk>j\n"
                f"<content>{diff.cotent}</content>\n"
                "<diffs>\n"
            )
            diffs += diff

        formatted_diffs.append(diff_header + diffs)

    return Prompt(
        "Using the information of the git diff in the " \
        "delimited triple backticks in xml format, write 3 conventional " \
        "commit messages.\n" \
        f"```\n {("").join(formatted_diffs)}\n```"
    )
    # Question: Should I created a dataclass for prompt -> Prompt(init_msg, formatted_diff)?
    
