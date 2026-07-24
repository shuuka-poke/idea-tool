from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request
from gensim.models import Word2Vec
import numpy as np
import random
import unicodedata

app = Flask(__name__)

app.secret_key = "好きな文字列を入れてください"
PASSWORD = "おひめ"

model = Word2Vec.load("wiki.model")


@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("login"):

        if request.method == "POST":

            if request.form.get("password") == PASSWORD:

                session["login"] = True
                return redirect(url_for("index"))

        return render_template("login.html")

    near_result = []
    far_result = []
    word = ""

    if request.method == "POST":

        word = request.form["word"]

        if word in model.wv:

            target = model.wv[word]

            distances = []

            for w in model.wv.index_to_key:

                if w != word:
                    if all(
                           unicodedata.category(c)[0] == "P"
                           for c in w
                           ):
                           continue

                    if all(
                           unicodedata.category(c)[0] == "N"
                           for c in w
                           ):
                         continue

                    distance = np.linalg.norm(target - model.wv[w])

                    distances.append((w, distance))

                    distances.sort(key=lambda x: x[1])

                    near_result = random.sample(
                        distances[:50],
                        min(5, len(distances[:50]))
                        )

                    far_result = random.sample(
                        distances[-50:],
                        min(5, len(distances[-50:]))
                        )

    return render_template(
        "index.html",
        word=word,
        near_result=near_result,
        far_result=far_result
    )

import os

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT",5000))
)
