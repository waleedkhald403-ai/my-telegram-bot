import os
import requests
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def get_updates(offset=None):
    url = TELEGRAM_URL + "/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = TELEGRAM_URL + "/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def ask_openai(message):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": message}],
    }
    response = requests.post(OPENAI_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text")
                    if text:
                        reply = ask_openai(text)
                        send_message(chat_id, reply)
        time.sleep(1)

if __name__ == "__main__":
    main()
