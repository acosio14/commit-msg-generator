import logging
from . import git_commands, formatter
from .parser import DiffParser

def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s %(levelname)s: %(messages)s",
    )

    diff_stats = git_commands.diff_num_stat()
    diff_name_status = git_commands.diff_name_status()
    diff_message = git_commands.diff()

    list_of_file_diffs = DiffParser(diff_stats, diff_name_status, diff_message).run()

    llm_prompt = formatter(list_of_file_diffs)