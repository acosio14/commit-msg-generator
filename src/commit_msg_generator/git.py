"""Thin wrapper around the git CLI.

This module runs git commands via subprocess and returns their output as
strings so the rest of the application (parser, llm, etc.) can work with
plain text. The two commands that matter for generating commit messages are:

    * git diff --staged  -> the changes we want to describe
    * git commit -m ...   -> record the change with the generated message

Notes on git behaviour worth remembering:
    * git refuses to commit without user.name and user.email configured.
    * Changes must be staged (``git add``) before they show up in --staged
      and before they can be committed.
"""

import subprocess


class GitError(RuntimeError):
    """Raised when a git command exits with a non-zero status."""


def _run(args: list[str]) -> str:
    """Run a git command and return its stdout as text.

    Raises GitError if git is not installed, the directory is not a repo,
    or the command exits non-zero.
    """
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise GitError("git is not installed or not on PATH") from exc

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise GitError(f"git {' '.join(args)} failed: {message}")

    return result.stdout


def is_repo() -> bool:
    """Return True if the current directory is inside a git work tree."""
    try:
        output = _run(["rev-parse", "--is-inside-work-tree"])
    except GitError:
        return False
    return output.strip() == "true"


def diff() -> str:
    """Return the staged diff as a string (``git diff --staged``)."""
    return _run(["diff", "--staged"])


def add(files: list[str] | None = None) -> None:
    """Stage files for commit. Stages everything when ``files`` is None."""
    targets = files if files else ["--all"]
    _run(["add", *targets])


def commit(msg: str) -> None:
    """Create a commit from the staged changes using ``msg`` as the message.

    Assumes changes are already staged (see ``add``). Raises GitError if
    there is nothing to commit or git is misconfigured.
    """
    _run(["commit", "-m", msg])
