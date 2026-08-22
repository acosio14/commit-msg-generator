from openrouter import OpenRouter
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

class CommitMsgError(ValueError):
    pass

FATAL = (
    BadRequestResponseError,
    UnauthorizedResponseError,
    ForbiddenResponseError,
    PayloadTooLargeResponseError, 
)

#Add Reroutes: TooManyRequestsResponseError, ProviderOverloadedResponseError, NotFoundResponseError, ResponseValidationError
# Not handling feat(api) / feat!:, use regex for this
# Need timeout error

RETRY = (
    CommitMsgError,
    json.JSONDecodeError,
    TooManyRequestsResponseError,
    InternalServerResponseError,
    BadGatewayResponseError,
    ServiceUnavailableResponseError,
)

class LLM:
    def __init__(self, default_model: list[str] = ["poolside/laguna-s-2.1:free"]):
        self.default_model = default_model
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
        models = self.default_model + self.fallback_models
        with OpenRouter(api_key=os.environ.get("OPENROUTER_API_KEY")) as client: 
            for model in models:
                for attempt in range(max_attempts):
                    try:
                        response = client.responses.send(
                            model = model,
                            response_format = { "type": "json_object"},
                            messages = [
                                {"role": "system", "content":
                                    "You are a senior software engineer. " \
                                    "Specializing in git conventional commits " \
                                    "and common software standards. " \
                                    "You generate concise conventional commit messages " \
                                    "based ONLY on the given `git diff` context. " \
                                    "The commit messages should be prefixed with one of following types: " \
                                    "fix, feat, build, chore, ci, docs, style, refactor, perf, test. " \
                                    "Keep commit message under 100 characters. " \
                                    "Do not include the prefix in the commit message character limit." \
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
                                },
                                {"role": "user",
                                 "content":
                                    f"Take the given git diff context in the delimited triple backticks and " \
                                    f"write a conventional commit message that summarizes all the changes " \
                                    f"being implemented in the code in one concise sentence. " \
                                    f"```{git_diff}```" \
                                }
                            ]
                        )

                        response_json =  json.loads(response.choices[0].message.content)
                        # Not every model support response type - json. Need per-model capability flag or 
                        # a graceful decay (if model doesn't support -> fallback to what?)

                        # if doesn't include prefix or less than 150 char -> fail
                        prefix_list = ["fix", "feat", "build", "chore", "ci", "docs", "style", "refactor", "perf", "test"]
                        prefix, msg = response_json["commit_message"].split(":", 1)
                        # The above could return KeyError if returns json with wrong shape (RETRY)
                        # TypeError if returned as list or string instead of dict. Validate the shape before indexing.
                        if prefix not in prefix_list:
                            raise CommitMsgError # will this and the below one crash? Need it to retry
                        
                        if len(msg) > 100:
                            raise CommitMsgError

                        return response_json

                    except FATAL as e: # These are fatal errors
                        raise LLMError from e

                    except RETRY as e: # These are retryable errors
                        print(f"Error: {e}")
                        time.sleep(2 ** attempt)
                        continue
        raise LLMError("All inputs exhausted")                