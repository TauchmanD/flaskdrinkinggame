from flask import Flask, session, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'asfdsafsdfadvasfgfhdfhgfasfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class user(db.Model):
	_id = db.Column('id', db.Integer(), primary_key=True)
	username = db.Column(db.String(20))
	password = db.Column(db.String())
	def __init__(self, username, password):
		self.username = username
		self.password = password
		



@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def homePage():
	return render_template('home.html')

@app.route('/register/', methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cPassword = request.form['confirmPass']
		if password == cPassword:
			usr = user(username, password)
			db.session.add(usr)
			db.session.commit()
			return redirect(url_for('homePage'))
		else:
			return render_template('register.html')
	else:
		return render_template('register.html')

if '__main__' == __name__:
	db.create_all()
	app.run(debug=True, host='0.0.0.0')
	