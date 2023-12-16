from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "springboard"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

boggle_game = Boggle()
set_words = set()

@app.route("/")
def home():
    """ Show the homepage and initialize some session keys. """

    tries = session.get("num_try", 0) + 1
    session["num_try"] = tries

    high_score = session.get("high_score", 0)
    session["high_score"] = high_score

    session["board"] = boggle_game.make_board()

    return render_template("home.html", game=session["board"], high_score=session["high_score"])

@app.route("/guess")
def guess():
    """ the route to check for valid and duplicate words. """

    guess_word = request.args["input_guess"]
    result = boggle_game.check_valid_word(session["board"], guess_word)

    if guess_word in set_words and result == "ok":
        result = "already guessed"
    elif result == "ok" and guess_word not in set_words:
        set_words.add(guess_word)

    return jsonify({"result": result})

@app.route("/score", methods=["POST"])
def score_and_try():
    """ a route to send and update some statistic about the game. """

    if request.json["total"] > session["high_score"]:
        session["high_score"] = request.json["total"]

    return jsonify({"high_score": session["high_score"],
                    "num_try": session["num_try"]})