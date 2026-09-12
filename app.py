import os
from flask import Flask, redirect
from pyrogram import Client

app = Flask(__name__)

# Render Environment variables se API details lenge
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# Pyrogram Client initialize karein
client = Client(
    "anime_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True,
)


@app.route("/")
def home():
  return "--> Telegram Stream Bridge Live 🌸 <--"


@app.route("/stream/<path:identifier>")
def stream_video(identifier):
  try:
    # Agar RubyVidHub ya koi aur link hai toh seedha redirect karo
    if "rubyvidhub.com" in identifier:
      return redirect(identifier)

    # Agar Telegram link hai ( jaise https://t.me/dekho_anime_here/2 )
    if "t.me" in identifier:
      parts = identifier.split("t.me/")[-1].split("/")
      channel = parts[0]
      msg_id = int(parts[1])

      if not client.is_connected:
        client.start()

      # Telegram channel se message fetch karo
      msg = client.get_messages(channel, msg_id)
      if msg and (msg.video or msg.document):
        media = msg.video or msg.document
        # Telegram CDN ka direct fast stream link generate karo
        file_url = client.get_file_link(media.file_id)
        return redirect(file_url)

    return "Media not found", 404
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
