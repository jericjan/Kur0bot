from flask import Flask, cli, request
from threading import Thread
#import sys
import requests

cli.show_server_banner = lambda *_: None
app = Flask("")


@app.route("/")
def home():
    return "Hello. I am alive!"


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/shutdown", methods=["POST"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."


def run():
    isRunning = False
    while isRunning == False:
        try:
            app.run(host="0.0.0.0", port=8080)
            isRunning = True
        except OSError as e:
            if e == "[Errno 98] Address already in use":
                print("Flask already running. Killing it.")
            requests.post("https://Kur0bot.jericjanjan.repl.co/shutdown")


def keep_alive():
    t = Thread(target=run)
    t.start()
