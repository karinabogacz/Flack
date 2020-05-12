import os
import requests
import json

from flask import Flask, render_template, json, jsonify, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "key"

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

data_json = {}

data_json["channels"] = []

@app.route("/", methods = ["GET", "POST"])
def index():

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

    return render_template("main.html", channels = data_json["channels"])

@socketio.on("create channel")
def channel(data):
    channel = data["channel"]
    data_json["channels"].append(channel) 
    emit("announce channel", {"data_json": data_json}, broadcast=True)

