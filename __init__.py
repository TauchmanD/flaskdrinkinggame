from flask import Flask, session, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from random import randint
import methods

app = Flask(__name__)
app.secret_key = 'asfdsafsdfadvasfgfhdfhgfasfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=20)


db = SQLAlchemy(app)

class user(db.Model):
	username = db.Column(db.String(20), unique=True, primary_key = True)
	password = db.Column(db.String())
	rounds = db.Column(db.Integer())
	drinksDrinked = db.Column(db.Integer())
	wantDrink = db.Column(db.Boolean())
	drinks = db.Column(db.Boolean())
	is_asking = db.Column(db.Boolean())
	is_answering = db.Column(db.Boolean())
	answer_drink = db.Column(db.Boolean())
	question = db.Column(db.String())
	answer = db.Column(db.String())
	def __init__(self, username, password, rounds, drinksDrinked, wantDrink, drinks, is_asking, is_answering, answer_drink, question, answer):
		self.username = username
		self.password = password
		self.rounds = rounds
		self.drinksDrinked = drinksDrinked
		self.wantDrink = wantDrink
		self.drinks = drinks
		self.is_answering = is_answering
		self.is_asking = is_asking
		self.answer_drink = answer_drink
		self.question = question
		self.answer = answer
		

@app.route('/', methods = ['GET','POST'])
def Login():
	if request.method == 'POST':
		session.permanent = True
		username = request.form['username']
		password = request.form['password']
		found_user = user.query.filter_by(username = username, password = password).first()
		if found_user:
			session['username'] = found_user.username
			return redirect(url_for('Home'))
	return render_template('login.html')

@app.route('/register/', methods = ['GET','POST'])
def Register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cPassword = request.form['confirmPass']
		if password == cPassword:
			usr = user(username, password, 0, 0, False, False, True, False, False,'','')
			db.session.add(usr)
			db.session.commit()
			return redirect(url_for('Login'))
		else:
			return render_template('register.html')
	else:
		return render_template('register.html')

@app.route('/home/', methods=["GET","POST"])
def Home():
	found_user = user.query.filter_by(username = session.get('username')).first()
	if request.method == 'POST':
		if found_user.wantDrink:
			found_user.wantDrink = False
			db.session.commit()
		else:
			found_user.wantDrink = True
			db.session.commit()
	return render_template('home.html', user = found_user)

@app.route('/asdasdgdasdfgsdfgsdbfjghbsdfgzhsdbfgolsdhzfgbdfosgbsdfghzbsdfgziuhboszdfziughbrtoguziadbsogf/', methods = ['GET', 'POST'])
def adminRound():
	users = user.query.all()
	return render_template('admin.html', users = users)

@app.route('/home/question', methods = ['GET','POST'])
def question_room():
	players = user.query.filter_by(wantDrink = True).all()
	return render_template('question_room.html', players = players)
@app.route('/home/question/<username>', methods = ['GET','POST'])
def question(username):
	usr = user.query.filter_by(username = username).first()
	usr.is_answering = True
	db.session.commit()
	if request.method == 'POST':
		question = request.form['question']
		usr.question = question
		db.session.commit()
	return render_template('question.html', user = usr)

if '__main__' == __name__:
	db.create_all()
	app.run(debug=True, host='0.0.0.0')
	