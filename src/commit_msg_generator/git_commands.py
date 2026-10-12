import subprocess
import logging

logger = logging.getLogger(__name__)


def diff_commands():
    diff_outputs = []
    diff_commands = ["--numstat", "--name-status", "--unified=0"]
    for command in diff_commands:
        output = subprocess.run(["git", "diff", "--staged", command], capture_output=True, text=True).stdout
        if len(output) == 0:
            logger.exception(
                f"error: 'git diff --staged {command}' returned empty string. "
                "Verify that changes are staged."
            )
        else:
            diff_outputs.append(output)
        
    return diff_outputs


def commit(msg: str) -> None:
    try:
        subprocess.run(["git", "commit", "-m", msg])
    except:
        logger.exception("error: commit msg")

# To-Do: 
# - Add unit test for git-commands
# - Figure out how to combine all functions into one; right now they are repeating (if I change one I change all)