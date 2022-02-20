from unittest import result
from flask import Flask, request, render_template, url_for, redirect, flash, Blueprint, session
from flask_pymongo import PyMongo
import mysql.connector

app = Flask(__name__)
flash_auth = Blueprint('auth', __name__)
app.secret_key = b'_5#y2L"H4Q8z\n\xec]/'

app.config["MONGO_URI"] = "mongodb://mongo_db:27017/analytics"
mongo = PyMongo(app)

auth_db = mysql.connector.connect(
  host="authentication",
  user="root",
  password="123",
  port="3306",
  database="authentication"
)

@app.route('/', methods=['GET'])
def show_results():
    results = mongo.db.statistics.find_one_or_404({"id": 1})

    min = results['min']
    max = results['max']
    mean = results['mean']

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        #response.headers['Cache-Control'] = 'no-cache'
        return render_template('results.html', min=min, max=max, mean=mean)

@app.route('/login')
def login():
    session["logged_in"] = False
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    auth_cursor = auth_db.cursor()
    auth_cursor.execute("SELECT * from users")
    
    auth_check = False
    for x in auth_cursor:
        if x[0] == username:
            if x[1] == password:
                auth_check = True

    if auth_check == True:
        flash("Login successful")
        session["logged_in"] = True
        return redirect(url_for("show_results"))
    else:
        flash("Login failed.")
        return redirect(url_for("login"))

@app.route('/register')
def register():
    session["logged_in"] = False
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register_post():
    username = request.form["username"]
    password = request.form["password"]

    auth_cursor = auth_db.cursor()
    
    add_user = True
    auth_cursor.execute("SELECT * FROM users")
    for x in auth_cursor:
        if x[0] == username:
            add_user = False

    if len(username) == 0 or len(password) == 0:
        flash("Please enter username and password.")
        return redirect(url_for("register"))


    if add_user == False:
        flash("User already exists.")
        return redirect(url_for("register"))
    else:
        query="INSERT INTO users VALUES(%s, %s)"
        auth_cursor.execute(query, (username, password))
        auth_db.commit()
        flash("Account created. Please login.")
        return redirect(url_for("login"))


@app.route('/logout', methods=["GET"])
def logout():
    flash("Successfully logged out")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)