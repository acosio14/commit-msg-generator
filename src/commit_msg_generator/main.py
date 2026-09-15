import logging
from . import git_commands, parser

def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s %(levelname)s: %(messages)s",
    )

    diff_stats = git_commands.diff_num_stat()
    diff_message = git_commands.diff()

    parsed_diff_msg = parser.run(diff_stats, diff_message)