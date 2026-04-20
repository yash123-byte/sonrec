import json
import random
import os
from datetime import timedelta
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import send_file, abort
import os
from google.cloud import storage
from datetime import timedelta
from google.cloud import storage
from google.oauth2 import service_account

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"

with open("vrushalimd.json") as f:
    songs = json.load(f)

class InfoForm(FlaskForm):
    user_name = StringField("Enter Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")
def get_song_data():
    item = random.choice(songs)
    song = item["song"]

    return {
        "song": song,
        "artist": item["artist"],
    }




@app.route("/", methods=["GET", "POST"])
def signin():
    form = InfoForm()

    if form.validate_on_submit():
        session["user_name"] = form.user_name.data.strip()
        return redirect(url_for("home"))

    return render_template("signin.html", form=form)


@app.route("/home")
def home():
    if "user_name" not in session:
        return redirect(url_for("signin"))

    return render_template("index.html", user_name=session["user_name"])


@app.route("/start")
def start():
    return jsonify(get_song_data())


@app.route("/recommend", methods=["POST"])
def recommend():    
        data = request.get_json(force=True)
        user = session.get("user_name", "anonymous")

        new_entry = {
            "artist": data.get("artist"),
            "song": data.get("song"),
            "preview_time": float(data.get("preview_time", 0)),
            "visits": int(data.get("visits", 1))
        }

        file_path = "a.json"
        with open(file_path, "r") as f:
            users_data = json.load(f)
        # If user doesn't exist, create empty list
        if user not in users_data:
            users_data[user] = []

        # Append new entry
        users_data["Yash"].append(new_entry)

        with open(file_path, "w") as f:
            json.dump(users_data, f, indent=4)   
        return jsonify(get_song_data())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

