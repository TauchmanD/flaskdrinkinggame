from flask import Flask, session, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def homePage():
	return render_template('home.html')

if '__main__' == __name__:
	app.run(debug=True, host='0.0.0.0')