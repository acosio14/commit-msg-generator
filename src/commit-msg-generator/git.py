# Run git diff
# Output stored in string variable
import subprocess

# git refuses commit without user.name and user.email
# when initializing a repo, .git/ is created
# changes need to be staged ("git add" or "git commit -a ...")
# git diff --staged
def diff():
    return subprocess.run(["git", "diff"], capture_output=True, text=True)

def commit(files: str, msg: str):
    # I use -a to add but if a new file is created it needs to be added
    # -> Need to check if new file needs to be staged and stage it
    # -> Maybe stage everything automatically
    # but what if I want to commit on certain files or divide commits. Need -i command

    if files == "":
        f = ""
    elif files == "all":
        f = "-a"
    else:
        for file in files:
            f += f"-i {file}"
        
    subprocess.run(["git", "commit", f, "-m", msg])