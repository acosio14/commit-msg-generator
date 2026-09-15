

def run(diff_stat: str, diff_message: str):

    stats = []
    for line in diff_stat.splitlines():
        added, deleted, filepath = line.split()
        stats.append(
            (int(added), int(deleted), str(filepath))
        )

    # Do something with stats
    
    
    