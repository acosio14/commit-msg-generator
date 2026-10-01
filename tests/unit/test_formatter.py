    # To-Do: Create Good path unit test for formatter
import pytest
from commit_msg_generator.parser import DiffParser, FileDiff, DiffContent
from commit_msg_generator.formatter import format_file_diffs

def test_format_file_diffs_one_line_modification_returns_prompt_with_xml_formatted_diff():
    # Arrange.
    diff_class = [
        FileDiff(
            "src/example.py",
            "Modified",
            {"added_lines": 1, "deleted_lines": 1},
            "diff --git a/src/example.py b/src/example.py\nindex f063189..a2dd04a 100644\n--- a/src/example.py\n+++ b/src/example.py\n",
            [
                DiffContent(
                    "@@ -91,4 +91 @@",
                    " class Addition:\n- a = 10\n+ a = 11"
                )
            ]
        )
    ]
    expected_prompt = (
        "Using the information of the git diff in the " \
        "delimited triple backticks in xml format, " \
        "write 3 conventional commit messages.\n" \
        "```\n"
        "<file>src/example.py</file>\n" \
        "<status>Modified</status>\n" \
        "<stats>" \
        "<added_lines>1</added_lines>" \
        "<deleted_lines>1</deleted_lines>" \
        "</stats>\n" \
        "<header>" \
        "diff --git a/src/example.py b/src/example.py\nindex f063189..a2dd04a 100644\n--- a/src/example.py\n+++ b/src/example.py\n" \
        "</header>\n" \
        "<diffs>\n" \
        "<hunk>@@ -91,4 +91 @@</hunk>\n" \
        "<content> class Addition:\n- a = 10\n+ a = 11</content>\n" \
        "</diffs>\n"
        "\n```"
    )

    # Act.
    prompt = format_file_diffs(diff_class)

    # Assert.
    assert prompt == expected_prompt
