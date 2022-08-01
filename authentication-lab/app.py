from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBlzb0mTG5Ye7yBvdQQoN4Y22Ko6q7_xZw",
  "authDomain": "mooo-f276e.firebaseapp.com",
  "projectId": "mooo-f276e",
  "storageBucket": "mooo-f276e.appspot.com",
  "messagingSenderId": "158138030076",
  "appId": "1:158138030076:web:d49819aefe97ec38258479",
  "measurementId": "G-T2N25R3Q3G",
  "databaseURL": "https://mooo-f276e-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session ["user"] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		full_Name=request.form("full_Name")
		username=request.form("User_Name")
		bio=request.form("bio")
		email = request.form['email']
		password = request.form['password']
		try:
			login_session ["user"] = auth.sign_in_with_email_and_password(email, password)
			user = {"user_name":username,"full_Name":full_Name,"bio":bio,"email":email,"password":password,}
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method =="POST":
		title=request.form("title")
		text=request.form("text")
		try:
			tweet={"title":title,"text":text}
			db.child("tweets").child(login_session['tweet']['localId']).set(user)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("add_tweet.html")




@app.route('/signout', methods=['GET', 'POST'])
def signout():
	error = ""

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session ["user"] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")

@app.route("/all_tweets")
def display_users():
    # Gets all the tweets from the database
    tweets = db.child("tweets").get().val()
    return render_template("tweets.html", tweets=tweets)


if __name__ == '__main__':
	app.run(debug=True)