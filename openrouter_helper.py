import requests
import json

def ask_openrouter(query):
    API_KEY = "your own API"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://riva.local",  # Optional
        "X-Title": "Riva Assistant"
    }

    payload = {
        "model": "deepseek/deepseek-r1-0528",
        "messages": [
            {"role": "system", "content": "You are a helpful AI coding assistant."},
            {"role": "user", "content": query}
        ],
        "max_tokens": 2048,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        res_json = response.json()
        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"].strip()
        elif "error" in res_json:
            return f"❌ OpenRouter Error: {res_json['error']['message']}"
        else:
            return "⚠️ Unknown error from OpenRouter."

    except Exception as e:
        return f"❌ Failed to connect: {e}"
