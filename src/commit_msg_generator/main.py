import logging
from commit_msg_generator import git_commands, formatter, llm_api
from commit_msg_generator.parser import DiffParser
from dotenv import load_dotenv

load_dotenv() 

def main():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s: %(messages)s",
    )

    diff_stats, diff_name_status, diff_message = git_commands.diff_commands()

    list_of_file_diffs = DiffParser(diff_stats, diff_name_status, diff_message).run()

    prompt = formatter.format_file_diffs(list_of_file_diffs)

    response = llm_api.send_prompt(prompt)

    print("Commit messages:")
    for i, commit in enumerate(response["commits"]):
        print(f"{i}) {commit}")
    print(f"{i+1}) None")
    print("\nSelect one: ")
    # To-Do: If 'None' selected. Give option to retry
    # To-Do: Add Custom/Manual option. For use to add their own message

    selected_index = int(input())
    if selected_index < i+1:
        git_commands.commit(response["commits"][selected_index])
    
if __name__ == "__main__":
    main()