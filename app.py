from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "springboard"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def home():
    session["board"] = boggle_game.make_board()
    print(session["board"])

    return render_template("home.html", game=session["board"])

@app.route("/guess")
def guess():

    guess_word = request.args["input_guess"]
    result = boggle_game.check_valid_word(session["board"], guess_word)

    print(guess_word, " : ", result)

    return jsonify({"result": result})
