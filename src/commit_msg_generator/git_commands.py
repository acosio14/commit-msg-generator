import subprocess
import logging

logger = logging.getLogger(__name__)


def diff_num_stat():
    diff_stat = subprocess.run(["git", "diff", "--staged", "--numstat"], capture_output=True, text=True).stdout
    if len(diff_stat) == 0:
        logger.exception(
            "error: git diff stats returned empty string. "
            "Verify that changes are staged."
        )
    else:
        return diff_stat

def diff_name_status():
    diff_name_status = subprocess.run(["git", "diff", "--staged", "--name-status"], capture_output=True, text=True).stdout
    if len(diff_name_status) == 0:
        
        logger.exception(
            "error: git diff name status returned empty string. "
            "Verify that changes are staged."
        )
    else:
        return diff_name_status

def diff() -> str:
    diff_msg = subprocess.run(["git", "diff", "--staged", "--unified=0"], capture_output=True, text=True).stdout
    if len(diff_msg) == 0:
        logger.exception(
            "error: git diff return empty string. "
            "Verify that changes are staged."
        )
    else:
        return diff_msg

def commit(msg: str) -> None:
    try:
        subprocess.run(["git", "commit", "-m", msg])
    except:
        logger.exception(
            "error: commit msg"
        )

# To-Do: 
# - Add unit test for git-commands
# - Figure out how to combine all functions into one; right now they are repeating (if I change one I change all)