from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)


# initialize page
@app.route("/init", methods=["POST"])
def init_survey():
    session["responses"] = []
    return redirect("/questions/1")


# Starting Page
@app.route("/")
def survey_start():
    """extract informations from the survey (title and instructions) and shows them on the starting page"""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("start.html", survey_title=title, survey_instructions=instructions)


# Question Pages
@app.route("/questions/<int:qID>")
def ask_question(qID):
    responses = session.get("responses")

    if qID <= len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[qID-1].question
        choices = satisfaction_survey.questions[qID-1].choices

    if (responses is None):
        flash("Trying to access question too early...", "error")
        return redirect("/")

    if qID != len(responses)+1:
        flash("Trying to access wrong question...", "error")
        return redirect(f"/questions/{len(responses)+1}")

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thankyou")

    return render_template("question.html", question=question, answers=choices, index=qID)


# Answer handling
@app.route("/answer", methods=["POST"])
def handle_answers():
    answer = request.form.get("answer")
    responses = session["responses"]

    if answer != None:
        responses.append(answer)
        session["responses"] = responses

        if len(responses) == len(satisfaction_survey.questions):
            return redirect("/thankyou")

    return redirect(f"/questions/{len(responses)+1}")


# Thankyou Page
@app.route("/thankyou")
def complete_page():

    return render_template("thankyou.html")
