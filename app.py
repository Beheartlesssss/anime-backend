import os
import requests
from flask import Flask, redirect

app = Flask(__name__)

BOT_TOKEN = "8786442663:AAFEDXAAEyy06AcnNeIE9bWeWm8JdrKPC08"


@app.route("/stream/<path:identifier>")
def stream_video(identifier):
  try:
    # Agar lamba URL ya path hai toh seedha Telegram web stream par redirect kar do
    if "dcld" in identifier or "http" in identifier or "/" in identifier:
      video_url = f"https://web.telegram.org/k/stream/{identifier}"
      return redirect(video_url)

    # Agar chota file_id hai toh Bot API se live link nikal lo
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={identifier}"
    response = requests.get(url).json()

    if "result" in response and "file_path" in response["result"]:
      file_path = response["result"]["file_path"]
      video_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
      return redirect(video_url)
    else:
      return f"Telegram Error: {response}", 400
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
