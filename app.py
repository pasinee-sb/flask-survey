from flask import Flask, render_template, request, redirect, jsonify, flash
from surveys import Question, Survey, satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


responses = []
ques_num =len(satisfaction_survey.questions)

@app.route("/")
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions=instructions)
    

@app.route("/questions/<int:num>")
def question(num):
    
    # if len(responses) ==0:
    #     return redirect(f"/questions/{num}")

    if (len(responses) != num):
        
        flash(f"invalid question page {num}",'error')
        return redirect(f"/questions/{len(responses)}")
    
    ques = satisfaction_survey.questions[num].question
    choices = satisfaction_survey.questions[num].choices
    num_ques = num+1
    return render_template("questions.html", survey_ques= ques, choices = choices, q= "Question number"+str(num_ques))

@app.route("/answer", methods= ["POST"])
def ans():
    responses.append(request.form["choice"])
    if (len(responses) == ques_num):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html",thanks="Thank you!")   
    