from flask import Flask, cli, send_from_directory
from threading import Thread
import os

cli.show_server_banner = lambda *_: None
app = Flask("")
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def home():
    return "Hello. I am alive!"

@app.route("/temp/<path>")
def send_report(path):
    return send_from_directory("temp", path)

def run():
    app.run(host="0.0.0.0", port=os.getenv("PORT"))

def keep_alive():
    t = Thread(target=run)
    t.start()
