import pytest
from commit_msg_generator.parser import DiffParser, FileDiff, DiffContent

"""
Tests
- 1 file modified / 1 change
- 1 file modified / 2 changes
- 1 file renamed
- 1 file added
- 1 file deleted
- 2 files modified / 1 change each
- 1 Very large file modified / 500 changes (uv.lock type)
- empty git msg, num_stat, and status
"""
def test_run_one_file_one_line_modification_return_FileDiff():
    # Arrange.
    diff_msg = (
        "diff --git a/src/example.py b/src/example.py\n"
        "index f063189..a2dd04a 100644\n"
        "--- a/src/example.py\n"
        "+++ b/src/example.py\n"
        "@@ -91,4 +91 @@ class Addition:\n"
        "- a = 10\n"
        "+ a = 11"
    )
    diff_stats = (
        "1       1       src/example.py"
    )
    diff_status = (
        "M       src/example.py"
    )
    diff_parser = DiffParser(diff_stats, diff_status, diff_msg)
    expected_diff_class = [
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

    # Act.
    list_of_file_diff = diff_parser.run()

    # Assert.
    assert list_of_file_diff == expected_diff_class