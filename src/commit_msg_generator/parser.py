import logging
import re

from .models import ChunkMsg, FileStatus, GitDiffMsg

log = logging.getLogger(__name__)


class DiffParseError(ValueError):
    """Raised when a diff cannot be parsed into chunks."""


# Compiled once at import (not per call) for efficiency.
_FILE_RE = re.compile(r"^diff --git a/(\S+) b/(\S+)")
_PLUSFILE_RE = re.compile(r"^\+\+\+ b/(\S+)")
_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
_RENAME_TO_RE = re.compile(r"^rename to (.+)$")
_COPY_TO_RE = re.compile(r"^copy to (.+)$")


def extract_git_diff(diff: str) -> GitDiffMsg:
    """Parse a unified git diff into per-hunk chunks, each tagged with status.

    Walks the diff line by line, tracking the current file (from ``diff --git`` /
    ``+++`` / ``rename to`` / ``copy to`` headers) and its :class:`FileStatus`
    (from ``new file`` / ``deleted file`` / ``rename`` / ``copy`` / ``Binary``
    headers). The body is split at each ``@@ ... @@`` hunk header into a
    :class:`ChunkMsg`.

    Every file yields at least one chunk. Files with no hunks — pure renames,
    deletions, binary changes, mode changes — emit a single header-only chunk
    (empty ``text``) so those changes are captured rather than silently dropped.

    Raises:
        DiffParseError: if ``diff`` is not a string, or a line cannot be parsed.
    """
    if not isinstance(diff, str):
        raise DiffParseError(f"expected a string diff, got {type(diff).__name__}")

    changes: list[ChunkMsg] = []

    current_file = ""
    current_start = 0
    current_status = FileStatus.MODIFIED
    current_lines: list[str] | None = None
    file_has_chunk = False
    file_count = 0

    def flush_hunk() -> None:
        nonlocal current_lines, file_has_chunk
        if current_lines is not None:
            changes.append(
                ChunkMsg(
                    file=current_file,
                    start_line_num=current_start,
                    text="\n".join(current_lines).rstrip(),
                    status=current_status,
                )
            )
            file_has_chunk = True
            current_lines = None

    def flush_file() -> None:
        # Close out the previous file: flush a pending hunk, and if the file
        # produced no hunk at all, still record it as a header-only chunk.
        flush_hunk()
        if current_file and not file_has_chunk:
            changes.append(
                ChunkMsg(
                    file=current_file,
                    start_line_num=0,
                    text="",
                    status=current_status,
                )
            )

    lineno, line = 0, ""
    try:
        for lineno, line in enumerate(diff.splitlines(), start=1):
            fm = _FILE_RE.match(line)
            if fm:
                flush_file()
                current_file = fm.group(2)  # b/ path (new name)
                current_start = 0
                current_status = FileStatus.MODIFIED
                current_lines = None
                file_has_chunk = False
                file_count += 1
                continue

            hm = _HUNK_RE.match(line)
            if hm:
                flush_hunk()
                current_start = int(hm.group(1))  # new-file start line
                current_lines = [line]
                continue

            if current_lines is not None:
                # Inside a hunk body.
                current_lines.append(line)
                continue

            # Extended header lines (before the first hunk) drive file status.
            if line.startswith("new file mode"):
                current_status = FileStatus.ADDED
            elif line.startswith("deleted file mode"):
                current_status = FileStatus.DELETED
            elif rm := _RENAME_TO_RE.match(line):
                current_status = FileStatus.RENAMED
                current_file = rm.group(1)
            elif cm := _COPY_TO_RE.match(line):
                current_status = FileStatus.COPIED
                current_file = cm.group(1)
            elif line.startswith("Binary files") and current_status is FileStatus.MODIFIED:
                current_status = FileStatus.BINARY
            elif pm := _PLUSFILE_RE.match(line):
                current_file = pm.group(1)
            # everything else (---, index, similarity, old/new mode) is ignored

        flush_file()
    except DiffParseError:
        raise
    except Exception as exc:
        raise DiffParseError(f"failed to parse diff at line {lineno}: {line!r}") from exc

    if diff.strip() and not changes:
        log.warning("Diff is non-empty but no files were parsed; unrecognized diff format")
    log.debug("Parsed %d file(s) into %d chunk(s)", file_count, len(changes))

    return GitDiffMsg(changes=changes, raw_text=diff)


def _count_changes(text: str) -> tuple[int, int]:
    """Count added/removed lines in a hunk body (ignores +++/--- file headers)."""
    added = removed = 0
    for line in text.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1
    return added, removed


def summarize(diff: GitDiffMsg) -> str:
    """Build a deterministic, one-glance summary of a diff — no API call.

    Aggregates the per-hunk chunks back to one line per file (status +
    added/removed counts), prefixed by an overall ``N files changed, +A/-D``
    tally. Cheap, reliable context for commit-message generation, and a natural
    fallback when a diff is too large to send whole to a model.
    """
    # file -> [status, additions, deletions]; dict preserves first-seen order.
    files: dict[str, list] = {}
    total_added = total_removed = 0

    for chunk in diff.changes:
        added, removed = _count_changes(chunk.text)
        total_added += added
        total_removed += removed
        entry = files.get(chunk.file)
        if entry is None:
            files[chunk.file] = [chunk.status, added, removed]
        else:
            entry[1] += added
            entry[2] += removed

    log.debug("Summarized %d chunk(s) across %d file(s)", len(diff.changes), len(files))

    if not files:
        return "No changes."

    lines = [f"{len(files)} file(s) changed, +{total_added}/-{total_removed}"]
    for path, (status, added, removed) in files.items():
        counts = f" (+{added}/-{removed})" if (added or removed) else ""
        lines.append(f"- {status:<8} {path}{counts}")
    return "\n".join(lines)
