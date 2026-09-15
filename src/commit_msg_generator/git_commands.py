import subprocess
import logging

logger = logging.getLogger(__name__)


def diff_num_stat():
    # Get stats to see what changes, see if too large to deal with. (added/deleted count)
    try:
        return subprocess.run(["git", "diff", "--staged", "--numstat"], capture_output=True, text=True).stdout
    except:
        logger.exception(
            "error: git diff stats"
        )

def diff_name_status():
    try:
        return subprocess.run(["git", "diff", "--staged","--name-status"], capture_output=True, text=True).stdout
    except:
        logger.exception(
            "error: git diff name status"
        )

def diff() -> str:
    # Show diff if staged
    try:
        return subprocess.run(["git", "diff", "--staged", "--unified=0"], capture_output=True, text=True).stdout
    except:
        logger.exception(
            "error: git diff return empty string."
            "verify that changes are staged."
        )

def commit(msg: str) -> None:
    try:
        subprocess.run(["git", "commit", "-m", msg])
    except:
        logger.exception(
            "error: commit msg"
        )

    