from openai import OpenAI
from openrouter.errors import (
    BadRequestResponseError,
    UnauthorizedResponseError,
    ForbiddenResponseError,
    PayloadTooLargeResponseError,
    TooManyRequestsResponseError,
    InternalServerResponseError,
    BadGatewayResponseError,
    ServiceUnavailableResponseError
)
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

class LLMError(Exception):
    pass


class LLM:
    def __init__(self, model: str = "poolside/laguna-s-2.1:free"):
        self.model = model


    def run_llm(self, git_diff: str, max_attempts: int = 4):
        models = self.model + fallback_models
        for model in models:
            for attempt in range(max_attempts):
                try:
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
                                "Keep commit message under 150 characters. " \
                                "Return a string in a json format structure, " \
                                "example shown in the delimited triple backticks:\n" \
                                f"""
                                '
                                {{
                                "response": 
                                    {{
                                    "commit_message": "fix: remove bug", 
                                    "model": "{model}"
                                    }}
                                }}
                                '
                                """
                                # Need error handling for when it doesn't return a json structure, retry
                                # Or if commit message not less than 150 char, or doesn't have prefix type
                            ),
                            input=(
                                f"Take the given git diff context in the delimited triple backticks and " \
                                f"write a conventional commit message that summarizes all the changes being implemented " \
                                f"in the code in one concise sentence. "
                                f"```{git_diff}```" \
                            )
                        )
                    return json.loads(response.output_text)


                except FATAL as e: # These are fatal errors
                    raise

                except json.JSONDecodeError as e: # These are retryable errors
                    print(f"Error: {e}")
                    time.sleep(2 ** attempt)
                    continue
            
            