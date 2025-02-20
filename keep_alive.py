# Module to run a webserver to keep the bot running

from threading import Thread

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.api_route("/", response_class=HTMLResponse, methods=["GET", "HEAD"])
def main() -> HTMLResponse:
	return HTMLResponse("Your bot is alive!")


def run() -> None:
	uvicorn.run(app, host="0.0.0.0", port=8080)


def keep_alive() -> None:
	server = Thread(target=run, daemon=True)
	server.start()
