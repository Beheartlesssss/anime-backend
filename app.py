import os
import requests
from flask import Flask, redirect

app = Flask(__name__)

# Tumhara Bot Token aur Channel ID yahan set hai
BOT_TOKEN = "7573887034:AAHLbY9p3S...bhi_jo_tumhara_token_hai..."
CHANNEL_ID = "@your_channel"


@app.route("/stream/<file_id>")
def stream_video(file_id):
  try:
    # Telegram API se file ka live path nikalna
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url).json()

    if "result" in response and "file_path" in response["result"]:
      file_path = response["result"]["file_path"]
      # Direct streaming URL generate karke redirect karna
      video_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
      return redirect(video_url)
    else:
      return "Invalid File ID or Bot Token", 400
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)