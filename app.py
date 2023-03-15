from flask import Flask, render_template, request, redirect, jsonify, flash, session
from surveys import Question, Survey, satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



ques_num =len(satisfaction_survey.questions)
res_session =[]

@app.route("/")
def home():
    session['responses'] = []
    
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions=instructions)
    

@app.route("/questions/<int:num>")
def question(num):
    res_session = session.get('responses')
    if (res_session is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(res_session) == ques_num):
        # They've answered all the questions! Thank them.
        return redirect("/thanks")

    if (len(res_session) != num):
        
        flash(f"invalid question page {num}",'error')
        return redirect(f"/questions/{len(res_session)}")
    
    ques = satisfaction_survey.questions[num].question
    choices = satisfaction_survey.questions[num].choices
    num_ques = num+1
    return render_template("questions.html", survey_ques= ques, choices = choices, q= "Question number"+str(num_ques))

@app.route("/answer", methods= ["POST"])
def ans():
    res_session = session['responses']
    res_session.append(request.form["choice"])
    session['responses'] = res_session
    
    
    if (len(res_session) == ques_num):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(res_session)}")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html",thanks="Thank you!")   
    