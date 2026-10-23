# To-Do: 
# - Look at a open-source repo and extract 20 different commits that span claudes list.
# - Store them in spreadsheet. 
# - Run app on each. Capture results. Add my pass/fail label with 'Why' note.
#     - Include time delay to get response in results
# - Group notes into failure modes.
# - For each failure mode decide how it can be checked. (script or LLM-as-judge)
from commit_msg_generator import main
from pathlib import Path


def eval():

    diff_cases_path = Path(".") / 'diff_cases'
    diff_cases = [ x for x in diff_cases_path.iterdir()]
    
    
    for case in diff_cases:
        msg = case / 'diff.txt'
        status = case / 'name-status.txt'
        numstat = case / 'numstat.txt'

        diff = []
        for file in [msg, status, numstat]:
            with open(file, 'r') as f:
                content = f.read()
            diff.append(content)

        main(eval=True, diff_case=diff)