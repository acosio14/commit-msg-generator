from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self, model: str):
        self.model = "poolside/laguna-s-2.1:free"


    def run_llm(self, git_diff: str):
        with OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY")
        ) as client:

            response = client.responses.create(
                model=self.model,
                instructions=(
                    "You are a senior software engineer. " \
                    "Specializing in git conventional commits " \
                    "and common software standards. " \
                    "You generate concise conventional commit messages " \
                    "based ONLY on the given `git diff` context. " \
                    "The commit messages should be prefixed with one of following types: " \
                    "fix, feat, build, chore, ci, docs, style, refactor, perf, test. " \
                    "Keep commit message under 150 characters. "
                    "Return in a json format structe, example shown in the delimited triple backticks:\n" \
                    f"""
                    ```
                    {{
                      response: 
                        {{
                          commit_message: "fix: remove bug", 
                          model: "{self.model}"
                        }}
                    }}
                    ```
                    """
                ),
                input=(
                    f"Take the given git diff context in the delimited triple backticks and " \
                    f"write a conventional commit message that summarizes all the changes being implemented " \
                    f"in the code in one concise sentence. "
                    f"```{git_diff}```" \
                )
            )

            return response.output_text