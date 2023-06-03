# Module to keep the bot alive

from waitress import serve
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main() -> None:
    return "Your bot is alive!"

def run() -> None:
    serve(app, host="0.0.0.0", port=10000)

def keep_alive() -> None:
    server = Thread(target=run, daemon=True)
    server.start()
