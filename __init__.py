from flask import Flask, session, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from random import randint
import methods
from  sqlalchemy.sql.expression import func, select

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
	drinks = db.Column(db.Integer())
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
			usr = user(username, password, 0, 0, False, 2, False, False, False,'','')
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
	players = user.query.filter_by(is_asking = False, wantDrink = True).all()
	if request.method == 'POST':
		return redirect(url_for('judging_room'))
	return render_template('question_room.html', players = players)





@app.route('/home/<username>', methods = ['POST', 'GET'])
def judging_room(username):
	usr = user.query.filter_by(username = username).first()
	asker = user.query.filter_by(is_asking = True).first()
	usrs = user.query.all()
	if request.method == 'POST':
		if request.form['pit'] == 'pit':
			usr.drinks = 1
			usr.drinksDrinked+=1
			usr.rounds+=1
		else:
			usr.drinks = 0
			usr.rounds+=1
		usr.question = ''
		asker.answer = ''
		usr.drinks = 2
		usr.is_answering = False
		for usr in usrs:
			usr.is_asking = False
			db.session.commit()
		new_asker = user.query.order_by(func.random()).first()
		new_asker.is_asking = True
		db.session.commit()
		return redirect(url_for('Home'))
	return render_template('judging_room.html', user=usr, asker=asker)

@app.route('/setAsker', methods = ['POST', 'GET'])
def set_asker():
	if request.method == 'POST':		
		usrs = user.query.all()
		for usr in usrs:
			usr.is_asking = False
			db.session.commit()
		new_asker = user.query.order_by(func.random()).first()
		new_asker.is_asking = True
		db.session.commit()
	return render_template('setAsker.html')



if '__main__' == __name__:
	db.create_all()
	app.run(debug=True, host='0.0.0.0')
	