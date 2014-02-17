#-------------------------------------------------------------------------------
# Name:        simplequiz
# Purpose:      to check knowledges
#
# Author:      Taras
#
# Created:     10.02.2014
# Copyright:   (c) Taras 2014
# Licence:     MIT Licence
#-------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, DateTime
import random
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5050/april_db'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

#-------------
# DB class
#-------------

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    firstname = db.Column(db.String(60), unique = True)
    secondname = db.Column(db.String(60), unique = True)
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, first_name, second_name, score, date):
        self.firstname = first_name
        self.secondname = second_name
        self.score = score
        self.date = date

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    text = db.Column(db.String(150), unique = True)
    question_id = db.Column(db.Integer, ForeignKey('questions.id'))
    correct = db.Column(db.Boolean)

    def __init__(self, text, question_id, correct):
        self.question_id = question_id
        self.text = text
        self.correct = correct

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    text = db.Column(db.String(150), unique = True)
    children = relationship("Answers", cascade="all,delete")

    def __init__(self, text):
        self.text = text

#-------------
# Function and methods
#-------------

@app.route('/home')
@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route('/quiz', methods = ['POST', 'GET'])
def quiz_page():
    if request.method == 'POST':
        summ = 0
        for i in range(5):
            if 'answer' + str(i) in request.form:
                if request.form['answer' + str(i)]:
                    summ = summ + 1
        User = Users(request.form['firstname'], request.form['secondname'], summ, datetime.utcnow())
        db.session.add(User)
        db.session.commit()
        return render_template('result.html', result = summ, name = request.form['firstname'], surname = request.form['secondname'])
    else:
        main_list = []
        questions = Questions.query.all()
        print len(questions)
        num = len(questions)
        questions = random.sample(questions, num)
        for i in range(len(questions)):
            part_list = []
            part_list.append(questions[i].text)
            answers = Answers.query.filter_by(question_id = questions[i].id).all()
            #answers = random.shuffle(answers)
            for j in range(len(answers)):
                part_list.append([answers[j].correct, answers[j].text])
            main_list.append(part_list)
        return render_template('quiz.html', questions = main_list)

@app.route('/admin', methods = ['POST', 'GET'])
def admin_page():
    if not('username' in session):
        return redirect(url_for('login_page'))
    else:
        mess = ""
        if request.method == 'POST':
            if 'delete_num' in request.form:
                if Questions.query.filter_by(id = request.form['delete_num']).first() is None:
                    mess = "No such question with id = " + str(request.form['delete_num'])
                else:
                    ques_to_delete = Questions.query.filter_by(id = request.form['delete_num']).first()
                    db.session.delete(ques_to_delete)
                    db.session.commit()
                    mess = "Question with id = " + str(request.form['delete_num']) + " was successfully deleted"
            else:
                Ques = Questions(request.form['question_text'])
                db.session.add(Ques)
                db.session.commit()
                question_id = Questions.query.filter_by(text = request.form['question_text']).first().id
                Answ = Answers(request.form['first_answer'], question_id, True)
                db.session.add(Answ)
                Answ = Answers(request.form['second_answer'], question_id, False)
                db.session.add(Answ)
                Answ = Answers(request.form['third_answer'], question_id, False)
                db.session.add(Answ)
                db.session.commit()
                mess = "Question was added successfully"
        return render_template('admin.html', questions = get_questions(), messege = mess)


def get_questions():
    questions = Questions.query.all()
    main_list = []
    for i in range(len(questions)):
        part_list = []
        part_list.append(questions[i].id)
        part_list.append(questions[i].text)
        answers = Answers.query.filter_by(question_id = questions[i].id).all()
        for j in range(len(answers)):
            part_list.append(answers[j].text)
        main_list.append(part_list)
    return main_list

@app.route('/login', methods = ['POST', 'GET'])
def login_page():
    if 'username' in session:
        return redirect(url_for('admin_page'))
    else:
        if request.method == 'POST':
            if (request.form['username'] == "Tester") & (request.form['pass'] == "quiztest"):
                session['username'] = [request.form['username'], request.form['pass']]
                return redirect(url_for('admin_page'))
            else:
                return render_template('logging.html', error_messege = "Invalid Login or Password. Try one more time")
        else:
            return render_template('logging.html', error_messege = "")

@app.route('/logout')
def logout_page():
    session.pop('username', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug = True)
