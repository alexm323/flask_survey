from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

RESPONSES = []


@app.route('/')
def show_survey_start():
    title = satisfaction_survey.title

    instructions = satisfaction_survey.instructions

    return render_template('survey_start.html', title=title, instructions=instructions)


@app.route('/begin', methods=["POST"])
def begin_survey():
    RESPONSES = []
    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def add_answer():
    survey_choice = request.form['answer']
    RESPONSES.append(survey_choice)

    if (len(RESPONSES) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(RESPONSES)}')


@app.route('/questions/<int:qid>')
def show_survey(qid):
    if(RESPONSES is None):
        return redirect('/')
    if(len(RESPONSES) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    if(len(RESPONSES) != qid):
        flash(f'Invalid question id: {qid}')
        return redirect(f'/questions/{len(RESPONSES)}')
    question = satisfaction_survey.questions[qid]

    return render_template('question.html', question=question, question_number=qid)


@app.route('/complete')
def complete():
    return render_template('completion.html')
