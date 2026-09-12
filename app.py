import os
import requests
from flask import Flask, redirect

app = Flask(__name__)


@app.route("/")
def home():
  return "--> Your service is live 🌸 <--"


@app.route("/stream/<path:identifier>")
def stream_video(identifier):
  try:
    # Agar Telegram post link hai toh use seedha redirect kar do
    if "t.me" in identifier:
      return redirect(identifier)

    # Agar lamba Telegram web stream URL hai
    if "dcld" in identifier or "http" in identifier or "/" in identifier:
      video_url = f"https://web.telegram.org/k/stream/{identifier}"
      return redirect(video_url)

    return "Invalid Link", 400
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
