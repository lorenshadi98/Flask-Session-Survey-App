
import surveys
from flask import Flask, render_template, request, redirect, flash, session
RESPONSES_KEY = "responses"

app = Flask(__name__)
responses = []
DESIRED_SURVEY = surveys.satisfaction_survey
SURVEY_SIZE = len(surveys.satisfaction_survey.questions)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def home_page():
    responses.clear()
    session[RESPONSES_KEY] = []
    survey_title = DESIRED_SURVEY.title
    survey_instructions = DESIRED_SURVEY.instructions
    return render_template("home.html", survey_title=survey_title, survey_instructions=survey_instructions)


@app.route("/question/<int:wanted_question>")
def survey_page(wanted_question):
    if wanted_question != len(responses):
        flash("You attempted to go to the wrong question.")
        return redirect(f"/question/{len(responses)}")
    else:
        survey_question = DESIRED_SURVEY.questions[wanted_question].question
        question_choices = DESIRED_SURVEY.questions[wanted_question].choices
        return render_template("survey_page.html", survey_question=survey_question, question_choices=question_choices)


@app.route("/answer", methods=["POST"])
def answer_page():
    response_ans = request.form["answer"]

    responses = session[RESPONSES_KEY]
    responses.append(response_ans)
    session[RESPONSES_KEY] = responses
    if len(responses) == SURVEY_SIZE:
        print("your responeses were", responses)
        print("Your session was", session[RESPONSES_KEY])
        return render_template("thank_you.html")
    else:
        redirect_url = f"/question/{len(responses)}"
        return redirect(redirect_url)
