import json
import uuid

import requests


def generate(prompt):
    first_headers = {
        "origin": "https://chat.openai.com",
        "referer": "https://chat.openai.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    session = requests.session()
    first_response = session.get("https://chat.openai.com/", headers=first_headers)
    oai_did = first_response.cookies.get("oai-did")

    token_headers = {
        "oai-device-id": oai_did,
        "origin": "https://chat.openai.com",
        "referer": "https://chat.openai.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    token_response = session.post("https://chat.openai.com/backend-anon/sentinel/chat-requirements", headers=token_headers)
    token = token_response.json()["token"]

    headers = {
        "oai-device-id": oai_did,
        "openai-sentinel-chat-requirements-token": token,
        "origin": "https://chat.openai.com",
        "referer": "https://chat.openai.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    json_data = {
        "action": "next",
        "messages": [
            {
                "id": str(uuid.uuid4()),
                "author": {
                    "role": "user",
                },
                "content": {
                    "content_type": "text",
                    "parts": [
                        prompt,
                    ],
                },
                "metadata": {},
            },
        ],
        "parent_message_id": str(uuid.uuid4()),
        "model": "text-davinci-002-render-sha",
        "timezone_offset_min": -540,
        "suggestions": [],
        "history_and_training_disabled": True,
        "conversation_mode": {
            "kind": "primary_assistant",
        },
        "force_paragen": False,
        "force_paragen_model_slug": "",
        "force_nulligen": False,
        "force_rate_limit": False,
        "websocket_request_id": str(uuid.uuid4()),
    }

    response = requests.post("https://chat.openai.com/backend-anon/conversation", headers=headers, json=json_data, stream=True)
    for line in response.iter_lines():
        line = line.decode("utf-8")
        if line and "[DONE]" not in line:
            json_data = json.loads(line.replace("data: ", ""))
            message = json_data["message"]["content"]["parts"][0]
            yield message
