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

FATAL = (
    BadRequestResponseError,
    UnauthorizedResponseError,
    ForbiddenResponseError,
)
RETRY = (
    json.JSONDecodeError,
    PayloadTooLargeResponseError, 
    TooManyRequestsResponseError,
    InternalServerResponseError,
    BadGatewayResponseError,
    ServiceUnavailableResponseError,
)

class LLM:
    def __init__(self, model: str = "poolside/laguna-s-2.1:free"):
        self.default_model = [model]
        self.fallback_models = [
            "z-ai/glm-5.2:free",
            "liquid/lfm-2.5-2.6b:free",
            "nvidia/nemotron-3.5-lightning:free",
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "google/gemma-4-26b-a4b-it:free",
            "google/gemma-4-31b-it:free",
            "openai/gpt-oss-20b:free"
            ]

    def run_llm(self, git_diff: str, max_attempts: int = 4) -> dict[str]:
        models = self.default_model.extend(self.fallback_models)
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
                                "model": "{model}",
                                "commit_message": "fix: remove bug"
                                }}
                                '
                                """
                                # Need error handling for when it doesn't return a json structure, retry
                                # Or if commit message not less than 150 char, or doesn't have prefix type
                            ),
                            input=(
                                f"Take the given git diff context in the delimited triple backticks and " \
                                f"write a conventional commit message that summarizes all the changes " \
                                f"being implemented in the code in one concise sentence. " \
                                f"```{git_diff}```" \
                            )
                        )
                    return json.loads(response.output_text)


                except FATAL as e: # These are fatal errors
                    raise

                except RETRY as e: # These are retryable errors
                    print(f"Error: {e}")
                    time.sleep(2 ** attempt)
                    continue
        raise ValueError("All inputs exhausted")    
            