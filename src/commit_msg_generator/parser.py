import re

def run(diff_stat: str, diff_file_status: str, diff_message: str):

    stats = []
    for line in diff_stat.splitlines():
        added, deleted, filepath = line.split()
        stats.append(
            (int(added), int(deleted), str(filepath))
        )

    name_status = []
    for line in diff_file_status.splitlines():
        status, file = line.split()
        name_status.append(
            (status, file)
        )

    diff_files = re.split(r'(?=diff)', diff_message)
    for file in diff_files:
        header, hunk, content = re.split(r"(@@[^@]+@@\n)", file)