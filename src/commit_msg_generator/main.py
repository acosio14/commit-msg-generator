import logging
from commit_msg_generator import git_commands, formatter, llm_api
from commit_msg_generator.parser import DiffParser
from dotenv import load_dotenv

load_dotenv() 

def main():
    logging.basicConfig(
        level=logging.WARNING, 
        format="%(asctime)s %(levelname)s: %(messages)s",
    )

    diff_stats = git_commands.diff_num_stat()
    diff_name_status = git_commands.diff_name_status()
    diff_message = git_commands.diff()

    list_of_file_diffs = DiffParser(diff_stats, diff_name_status, diff_message).run()

    prompt = formatter.format_file_diffs(list_of_file_diffs)

    llm_api.send_prompt(prompt)
    
if __name__ == "__main__":
    main()