import logging
from commit_msg_generator.parser import FileDiff
from dataclasses import asdict
import json

logger = logging.getLogger(__name__)


# from parser:
# [ FileDiff(filename, status, stats, header, [ DiffContent(hunk, content) ]) ]
    # Make a json formatted object?
def convert_file_diff_to_json_format(list_file_diffs: FileDiff):
    for file_diff in list_file_diffs:
        file_diff_json = json.dumps(asdict(file_diff))


def create_llm_prompt():

    initial_prompt = (
        "Using the information on the git diff below in the " \
        "delimited triple backticks, write 3 conventional " \
        "commit messages."
    )

