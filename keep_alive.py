# Module to keep the bot alive

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main() -> None:
    return "Your bot is alive!"

def run() -> None:
    app.run(host="0.0.0.0", port=8080)

def keep_alive() -> None:
    server = Thread(target=run)
    server.start()
