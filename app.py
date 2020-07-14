from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)




@app.route('/')
def show_survey_start():
    title = satisfaction_survey.title

    instructions = satisfaction_survey.instructions

    return render_template('survey_start.html', title=title, instructions=instructions)


@app.route('/begin', methods=["POST"])
def begin_survey():
    session['response_key'] = []
    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def add_answer():
    responses = session['response_key']

    survey_choice = request.form['answer']
   
    responses.append(survey_choice)

    session['response_key'] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/questions/<int:qid>')
def show_survey(qid):
    responses = session.get('response_key')

    if(responses is None):
        return redirect('/')

    if(len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    if(len(responses) != qid):
        flash(f'Invalid question id: {qid}.')
        return redirect(f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[qid]

    return render_template('question.html', question=question, qid=qid)


@app.route('/complete')
def complete():
    return render_template('completion.html')
