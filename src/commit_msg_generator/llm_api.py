from openrouter import OpenRouter
from openrouter.errors import(
    TooManyRequestsResponseError,
)
import os
from commit_msg_generator.formatter import Prompt
import json
import logging

logger = logging.getLogger(__name__)
# To-Do: 
# - Find way to get models to correctly select the right type of commit (show examples?)
# - Look to improve latency. Make response faster. See https://developers.openai.com/api/docs/guides/latency-optimization
# - Add unit test for llm_api. Good path, 429 error handling, all models tried handling
# - Include model in return prompt.

MODELS = [
    "apodex/apodex-1.1-mini:free",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "google/gemma-4-31b-it:free",
    "liquid/lfm-2.5-2.6b:free",
    "thinkingmachines/inkling-small:free",
]

def send_prompt(prompt: Prompt, model_index: int = 0):
    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
        try:
            response = client.chat.send(
                model=MODELS[model_index],
                messages=[
                    {"role": "system", "content": "You are a conventional commit generator."},
                    {"role": "user", "content": f"{prompt.msg}"}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except TooManyRequestsResponseError as error:
            logger.exception(f"{error}. Retrying llm api call.")
            if model_index <= len(MODELS):
                send_prompt(Prompt, model_index+1)
            else:
                print("All models tried.")

