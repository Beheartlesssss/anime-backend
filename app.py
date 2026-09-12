import os
import re
import requests
from flask import Flask, Response, redirect

app = Flask(__name__)


@app.route("/")
def home():
  return "--> Your service is live 🌸 <--"


@app.route("/stream/<path:identifier>")
def stream_video(identifier):
  try:
    # Agar RubyVidHub link hai toh seedha redirect karo
    if "rubyvidhub.com" in identifier:
      return redirect(identifier)

    # Agar Telegram post link hai
    if "t.me" in identifier:
      # Telegram web page se HTML fetch karo
      headers = {
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
              " like Gecko) Chrome/120.0.0.0 Safari/537.36"
          )
      }
      resp = requests.get(identifier, headers=headers)

      if resp.status_code == 200:
        # HTML ke andar se direct video file (.mp4) ka link dhoondo
        match = re.search(r'property="og:video"\s+content="([^"]+)"', resp.text)
        if not match:
          match = re.search(
              r'src="([^"]+\.mp4(?:\?[^"]*)?)"', resp.text, re.IGNORECASE
          )

        if match:
          video_url = match.group(1)
          # Agar relative link hai toh domain jod do
          if video_url.startswith("/"):
            video_url = "https://t.me" + video_url
          return redirect(video_url)

        # Agar direct og:video nahi mila, toh t.me embed/og meta check karo
        match_alt = re.search(
            r'<meta property="og:video:secure_url" content="([^"]+)"', resp.text
        )
        if match_alt:
          return redirect(match_alt.group(1))

      # Fallback: Agar kuch extract na ho paaye toh seedha page par bhej do
      return redirect(identifier)

    return "Invalid Link", 400
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
