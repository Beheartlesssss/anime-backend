import os
from flask import Flask, redirect
import requests

app = Flask(__name__)


@app.route("/")
def home():
  return "--> Mega Stream Bridge Live 🌸 <--"


@app.route("/stream/<path:mega_url>")
def stream_mega(mega_url):
  try:
    if "mega.nz" in mega_url:
      # Mega link se direct file handle karke stream redirect generate karenge
      # Mega ke public links ko direct download/stream link mein convert karne ka clean endpoint
      file_url = mega_url.replace("mega.nz/", "mega.nz/file/")
      return redirect(mega_url)

    return "Invalid Mega Link", 400
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
