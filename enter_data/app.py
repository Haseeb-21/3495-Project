from flask import Flask, request, render_template, url_for, redirect, flash, Blueprint, session
from flask_mysqldb import MySQL
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from authentication import auth
import yaml

app = Flask(__name__)
flash_auth = Blueprint('auth', __name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

with open('mysql.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())
    app.config['MYSQL_USER'] = app_config['datastore']['user']
    app.config['MYSQL_PASSWORD'] = app_config['datastore']['password']
    app.config['MYSQL_DB'] = app_config['datastore']['db']
    app.config['MYSQL_HOST'] = app_config['datastore']['hostname']
    mysql = MySQL(app)


@app.route('/', methods=['GET'])
def data_entry():
    cur = mysql.connection.cursor()            # updates default values
    cur.execute("SELECT * FROM grades")
    data = cur.fetchall()
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        #response.headers['Cache-Control'] = 'no-cache'
        return render_template('home.html', data=data)
    
    
    

@app.route('/', methods=['POST'])
def date_entry_post():
    grades_list = {}
    i = 1

    while i <= 7:
        course = request.form[f"course{i}"]
        grade = request.form[f"grade{i}"]
        if grade.isdigit():
            grades_list[course] = float(grade)
            i += 1
            if float(grade) > 100 or float(grade) < 0:
                flash("❌⚠️ Grades must be in range of 0-100")
                return redirect(url_for("data_entry"))
        elif grade == "":
            break
        else:
            flash("❌⚠️ Grades should be numeric values")
            return redirect(url_for("data_entry"))

    
    if len(grades_list) != 7:
            flash("❌⚠️ Please enter a grade for all courses")
            return redirect(url_for("data_entry"))

    else:
        cur = mysql.connection.cursor()
        #query="insert into grades(course, grade) values(%s,%s)"            # insert query
        query="update grades set course = %s, grade = %s where id = %s"     # update query

        id = 1
        for item in grades_list.items():
            #cur.execute(query, (item[0],item[1]))       # inserts into db
            cur.execute(query, (item[0],item[1],id))    # alters existing entries
            mysql.connection.commit()
            id+=1

        flash("✅ Grades updated successfully")
        return redirect(url_for("data_entry"))


@app.route('/login')
def login():
    session["logged_in"] = False
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    auth_check = auth.check_auth(username, password)
    if auth_check == True:
        flash("Login successful")
        session["logged_in"] = True
        return redirect(url_for("data_entry"))
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

    if len(username) == 0 or len(password) == 0:
        flash("Please enter username and password.")
        return redirect(url_for("register"))

    add_user = auth.add_user(username, password)
    if add_user == False:
        flash("Username already exists.")
        return redirect(url_for("register"))
    else:
        flash("Account created. Please login.")
        return redirect(url_for("login"))


"""@app.route('/logout', methods=["POST"])
def logout():
    print("e")
    flash("Successfully logged out")
    return redirect(url_for("login"))"""
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)