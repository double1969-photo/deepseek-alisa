import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    response = requests.post(
        DEEPSEEK_API_URL,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": user_text}],
        }
    )
    response_data = response.json()
    choices = response_data.get("choices")

    if not choices or not isinstance(choices, list) or len(choices) == 0:
        error_info = response_data.get("error", {}).get("message", "Неизвестная ошибка API")
        answer = f"Ошибка при обращении к DeepSeek: {error_info}"
    else:
        answer = choices[0]["message"]["content"]
    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
