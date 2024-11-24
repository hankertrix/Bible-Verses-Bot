# Module to keep the bot alive

from threading import Thread

from flask import Flask
from waitress import serve

app = Flask("")


@app.route("/")
def main() -> str:
    return "Your bot is alive!"


def run() -> None:
    serve(app, host="0.0.0.0", port=8080)


def keep_alive() -> None:
    server = Thread(target=run, daemon=True)
    server.start()
