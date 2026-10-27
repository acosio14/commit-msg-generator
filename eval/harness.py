# To-Do: 
# - Look at a open-source repo and extract 20 different commits that span claudes list.
# - Store them in spreadsheet. 
# - Run app on each. Capture results. Add my pass/fail label with 'Why' note.
#     - Include time delay to get response in results
# - Group notes into failure modes.
# - For each failure mode decide how it can be checked. (script or LLM-as-judge)
from commit_msg_generator.main import main
from pathlib import Path


def _eval():

    diff_cases_path = Path("eval") / 'diff_cases'
    diff_cases = [ x for x in diff_cases_path.iterdir()]
    
    
    for case in diff_cases:
        numstat = case / 'numstat.txt'
        status = case / 'name-status.txt'
        msg = case / 'diff.txt'

        diff = []
        for input_file in [numstat, status, msg]:
            with open(input_file, 'r') as f:
                content = f.read()
            diff.append(content)

        model, commits = main(eval=True, diff_case=diff)

        output_file = case / "results.txt"
        # To-Do: handle multiple runs. Do I replace results file or add new one. (FileExistError)
        with open(output_file, 'w') as f:
            f.write(f"{model}\n")
            f.writelines(f"{commits}\n")


if __name__ == "__main__":
    _eval()

# To-Do:
# - How do I store/capture/file the output for all cases in the loop