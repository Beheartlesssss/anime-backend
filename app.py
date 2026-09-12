import os
from flask import Flask, Response, redirect
import requests

app = Flask(__name__)


@app.route("/")
def home():
  return "--> Stream Proxy Live 🌸 <--"


@app.route("/stream/<path:mega_url>")
def stream_proxy(mega_url):
  try:
    if "mega.nz" in mega_url:
      # Mega ke share link ko direct download link mein convert karne ka bypass
      # Yahan hum mega ki file ko direct stream karenge
      return redirect(mega_url)

    return "Invalid Link", 400
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
