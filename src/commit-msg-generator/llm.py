from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

response = client.responses.create(
    model="poolside/laguna-s-2.1:free",
    instructions=(
        "You are a senior software engineer. " \
        "Specializing in git conventional commits " \
        "and common software standards." \
        "You generate concise conventional commit messages " \
        "based ONLY on the git diff context given." \
        "The commit messages should prefixed with one of following types: " \
        "fix, feat, build, chore, ci, docs, style, refactor, perf, test "
    ),
    input=(
        f"Take the given git diff context in the delimited triple backticks and " \
        f"write a conventional commit message that summarizes all the changes being implemented " \
        f"in the code in one concise sentence. "
        f"Keep commit message under 150 characters.```{git_diff_context}```"
    )
)

print(response.output_text)

