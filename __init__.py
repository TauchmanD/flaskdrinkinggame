from flask import Flask, session, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'asfdsafsdfadvasfgfhdfhgfasfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=20)


db = SQLAlchemy(app)

class user(db.Model):
	_id = db.Column('id', db.Integer(), primary_key=True)
	username = db.Column(db.String(20), unique=True)
	password = db.Column(db.String())
	rounds = db.Column(db.Integer())
	drinksDrinked = db.Column(db.Integer())
	wantDrink = db.Column(db.Boolean())
	drinks = db.Column(db.Boolean())
	def __init__(self, username, password, rounds, drinksDrinked, wantDrink, drinks):
		self.username = username
		self.password = password
		self.rounds = rounds
		self.drinksDrinked = drinksDrinked
		self.wantDrink = wantDrink
		self.drinks = drinks
		



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
			usr = user(username, password, 0, 0, False, False)
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

if '__main__' == __name__:
	db.create_all()
	app.run(debug=True, host='0.0.0.0')
	