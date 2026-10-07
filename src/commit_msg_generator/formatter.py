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
            f"<file>{file_diffs.file}</file>\n"
            f"<status>{file_diffs.status}</status>\n"
            f"<stats><added_lines>{file_diffs.stats["added_lines"]}</added_lines>"
            f"<deleted_lines>{file_diffs.stats["deleted_lines"]}</deleted_lines></stats>\n"
            f"<header>{file_diffs.header}</header>\n"
        )
        diffs = ""
        for diff in file_diffs.diffs:
            diff = (
                "<diffs>\n"
                f"<hunk>{diff.hunk}</hunk>\n"
                f"<content>{diff.content}</content>\n"
                "</diffs>\n"
            )
            diffs += diff

        formatted_diffs.append(diff_header + diffs)

    types = (
        """Types
- `feat` Commits that add, adjust or remove a feature
- `fix` Commits that fix bug of a preceded `feat` commit
- `refactor` Commits that rewrite or restructure code without altering API or UI behavior
- `perf` Commits are special type of `refactor` commits that specifically improve performance
- `style` Commits that address code style (e.g., white-space, formatting, missing semi-colons) and do not affect application behavior
- `test` Commits that add missing tests or correct existing ones
- `docs` Commits that exclusively affect documentation
- `build` Commits that affect build-related components such as build tools, dependencies, project version, ...
- `ops` Commits that affect operational aspects like infrastructure (IaC), deployment scripts, CI/CD pipelines, backups, monitoring, or recovery procedures, ...
- `chore` Commits that represent tasks like initial commit, modifying `.gitignore`, ..."""
    )

    return Prompt(
        msg = (
            "Use the information of the git diff in the " \
            "delimited triple backticks in xml format to, " \
            "write 3 conventional commit messages.\n" \
            f"They should be one of the following types:\n {types}\n"
            "Return a JSON formatted output of an" \
            "unnumbered ordered list. Ouput format should" \
            "look like the following example:\n" \
            "{\n"
            "'commits':\n"
            "  [\n"
            "    'feat: commit msg one',\n"
            "    'feat: commit msg two',\n"
            "    'feat: commit msg three'\n"
            "  ]\n" \
            "}\n" \
            f"```\n{("").join(formatted_diffs)}\n```"
        )
    )
    
