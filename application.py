import os
import requests

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "key"

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods = ["GET", "POST"])
def index():
    #User can only sign by post request
    if request.method == "POST": 

        username = request.form.get("username")
        
        if username == "":
            message = "You need to provide username"
            return render_template("index.html", message = message)

        session["user"] = username

        if "user" in session:
            return redirect(url_for("channels"))

    return render_template("index.html")

@app.route("/channels")
def channels():

    if "user" not in session:
        return redirect(url_for("index"))

    return render_template("main.html")

