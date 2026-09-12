import os
import requests
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = "8786442663:AAFEDXAAEyy06AcnNeIE9bWeWm8JdrKPC08"


@app.route("/")
def get_file_id():
  # Yeh link kholte hi bot par aakhri aayi video ka file_id seedha screen par dikha dega!
  url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
  res = requests.get(url).json()
  try:
    # Aakhri message se file_id nikalna
    for result in reversed(res.get("result", [])):
      message = result.get("message", {})
      if "video" in message:
        return f"MIL GAYA FILE ID: <br><br><b>{message['video']['file_id']}</b>"
      elif "document" in message:
        return (
            "MIL GAYA FILE ID:"
            f" <br><br><b>{message['document']['file_id']}</b>"
        )
    return (
        "Bot par koi video nahi mili! Pehle apne bot ko video bhejo phir yeh link"
        " refresh karo."
    )
  except Exception as e:
    return str(e)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
