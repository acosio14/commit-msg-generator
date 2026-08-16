from types import GitDiffMsg, ChunkMsg
import re


def extract_git_diff(diff: str) -> GitDiffMsg:
    """Parse a unified git diff into per-hunk chunks.

    Walks the diff line by line, tracking the current file (from
    ``diff --git`` / ``+++`` headers) and splitting the body at each
    ``@@ ... @@`` hunk header. Each hunk becomes a ChunkMsg carrying its
    file path, the new-file start line, and the hunk text.
    """
    file_re = re.compile(r"^diff --git a/(\S+) b/(\S+)")
    plusfile_re = re.compile(r"^\+\+\+ b/(\S+)")
    hunk_re = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")

    changes: list[ChunkMsg] = []
    current_file = ""
    current_start = 0
    current_lines: list[str] | None = None

    def flush():
        if current_lines is not None:
            changes.append(
                ChunkMsg(
                    file=current_file,
                    start_line_num=current_start,
                    text="\n".join(current_lines).rstrip(),
                )
            )

    for line in diff.splitlines():
        fm = file_re.match(line)
        if fm:
            flush()
            current_lines = None
            current_file = fm.group(2)  # b/ path (new name)
            continue

        pm = plusfile_re.match(line)
        if pm:
            current_file = pm.group(1)
            continue

        hm = hunk_re.match(line)
        if hm:
            flush()
            current_start = int(hm.group(1))  # new-file start line
            current_lines = [line]
            continue

        if current_lines is not None:
            current_lines.append(line)

    flush()

    return GitDiffMsg(changes=changes, raw_text=diff)