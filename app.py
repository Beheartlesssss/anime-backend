import os
from flask import Flask, redirect
from mega import Mega

app = Flask(__name__)

# Mega client initialize karein (anonymous login)
mega = Mega()
m = mega.login()


@app.route("/")
def home():
  return "--> Mega Stream Bridge Live 🌸 <--"


@app.route("/stream/<path:mega_url>")
def stream_mega(mega_url):
  try:
    # Agar URL mein full mega link hai
    if "mega.nz" in mega_url:
      # Mega file link se direct streaming/download link generate karo
      file_link = m.get_link(mega_url)
      return redirect(file_link)

    return "Invalid Mega Link", 400
  except Exception as e:
    return str(e), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
