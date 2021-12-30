from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# Constants created for responses
RESPONSES = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "yupp1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def show_survey():
    """Select Desired Survey"""
    return render_template("start.html", survey=survey)


@app.route('/begin', methods=["POST"])
def begin_survery():
    """Clear session of started survey"""
    session[RESPONSES] = []
    return redirect("/questions/0")


@app.route('/answer', methods=["POST"])
def handle_question():
    """Save response, and move to next question"""
    responses = session.get(RESPONSES)

    if ("answer" in request.form):
        # Get response
        choice = request.form['answer']

    else:
        flash("Please answer the question before continuing")
        return redirect(f"/questions/{len(responses)}")

        # Add response to session.
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        # All questions are answered.
        return redirect("/completed")

    else:
        return redirect(f"/questions/{len(responses)}")


@ app.route('/questions/<int:qid>')
def show_question(qid):
    """Display Current Question"""
    responses = session.get(RESPONSES)

    if (responses is None):
        # trying to access quesitons.
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        # All questions are answered.
        return redirect('/completed')

    if (len(responses) != qid):
        # Accessing questions out of order
        flash(f"Invalid questions: {qid}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("questions.html", question_num=qid, question=question)


@ app.route('/completed')
def complete():
    """Survey complete. Show completed survey."""
    return render_template("completed.html")
