import json
from commit_msg_generator.formatter import Prompt
from commit_msg_generator.llm_api import send_prompt
from unittest.mock import MagicMock, patch

# To-Do:
# - Add unit test for llm_api. Good path, 429 error handling, all models tried handling.
#   Use mocking to fake api call.
# - Fix unit test error: UnauthorizedResponseError (probably Keys, Mock them)

def test_send_prompt_with_good_response_return_success(monkeypatch):
   
    # Arrange.
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-123")
    prompt = Prompt("Hi")
    model_index = 0
    expected_response = ({"msg": "Hi"}, "llm/model:free")

    # Act.
    with patch("commit_msg_generator.llm_api.OpenRouter") as mock_openrouter:
        client = mock_openrouter.return_value.__enter__.return_value
        response  = client.chat.send.return_value
        response.choices[0].message.content = json.dumps({"msg": "Hi"})
        response.model = "llm/model:free"

        result  = send_prompt(prompt, model_index)

    # Assert.
    assert result == expected_response