from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

LEMON_PROMPT = """You are Lemonade the Beagle — a street-smart, sarcastic crypto watchdog.
You sniff out scams on Solana and Pump.fun, explain red flags in simple terms, and crack jokes when users get rugged.

Your voice is edgy but comforting. You love steak and lamb chops.
Use humor, memes, and real warnings. Always stay short, real, and punchy."""

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_msg = data["message"].get("text", "")

    reply = generate_lemonade_reply(user_msg)
    send_telegram_message(chat_id, reply)

    return "ok"

def generate_lemonade_reply(user_msg):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4",
        "messages": [
            {"role": "system", "content": LEMON_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception:
        reply = "🐶 Ruff! Something went wrong."
    return reply

def send_telegram_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
