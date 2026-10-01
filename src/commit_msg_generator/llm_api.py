from openrouter import OpenRouter
import os
from commit_msg_generator.formatter import Prompt

def send_prompt(prompt: Prompt):

    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
        response = client.chat.send(
            model="qwen/qwen3.8-27b:free",
            messages=[
                {"role": "user", "content": {prompt}}
            ],
        )

        print(response.choices[0].message.content)