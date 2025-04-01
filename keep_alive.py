from flask import Flask, cli, send_from_directory  # type: ignore
from threading import Thread
import os

cli.show_server_banner = lambda *_: None  # type: ignore
app = Flask("")
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def home():
    return "Hello. I am alive!"


@app.route("/temp/<path>")
def send_report(path: str):
    return send_from_directory("temp", path)


def run():
    if port := os.getenv("PORT"):
        app.run(host="0.0.0.0", port=int(port))
    else:
        print("There is no PORT specified in your env variables.")


def keep_alive():
    t = Thread(target=run)
    t.start()
