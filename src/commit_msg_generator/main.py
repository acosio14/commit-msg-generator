import logging
from . import git_commands, parser

def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s %(levelname)s: %(messages)s",
    )

    diff_message = git_commands.diff()

    parsed_diff_msg = parser.run(diff_message)