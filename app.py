from surveys import satisfaction_survey
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "springboard"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """ Home page of the app """

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("home.html", title=title, instructions=instructions)

@app.route("/setup_session", methods=["POST"])
def session_route():
    session["responses"] = []
    return redirect("/question/0")

@app.route("/question/<int:num>")
def question(num):
    """ Show a form asking question for the survey """

    if len(session["responses"]) != num:
        flash("You are trying to access an invalid question", "error")
        q_num = len(session["responses"])
        return redirect(f"/question/{q_num}")

    num = len(session["responses"])
    question = satisfaction_survey.questions[num -1]

    if num == len(satisfaction_survey.questions):
        return redirect("/completed")

    if num < len(satisfaction_survey.questions):
        return render_template("question.html", num=num+1, question=question)

@app.route("/answer", methods=["POST"])
def answer():
    """ Handle the user answers / add the answers to the responses[] """

    num = len(session["responses"])
    if num == len(satisfaction_survey.questions):
        return redirect("/completed")

    answer = request.form["answer"]

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    return redirect(f"/question/{num+1}")

@app.route("/completed")
def completed():
    """ Show the completed page when the user has answered all the questions """
    return render_template("completed.html")
