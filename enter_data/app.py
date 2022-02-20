from flask import Flask, request, render_template, url_for, redirect, flash, Blueprint, session
import mysql.connector

app = Flask(__name__)
flash_auth = Blueprint('auth', __name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mydb = mysql.connector.connect(
  host="mysql_db",
  user="root",
  password="123",
  port="3306",
  database="grades"
)

auth_db = mysql.connector.connect(
  host="authentication",
  user="root",
  password="123",
  port="3306",
  database="authentication"
)


cursor = mydb.cursor()
cursor.execute("SHOW TABLES")
for x in cursor:
    pass

try:
    cursor.execute(''' 
                CREATE TABLE grades (
                id INT NOT NULL AUTO_INCREMENT,
                course VARCHAR(45) NOT NULL,
                grade INT NOT NULL,
                PRIMARY KEY (id));
            ''')            
    cursor.execute("insert into grades(course, grade) values('ACIT3495', 0)")
    cursor.execute("insert into grades(course, grade) values('ACIT3855', 0)")
    cursor.execute("insert into grades(course, grade) values('ACIT4640', 0)")
    cursor.execute("insert into grades(course, grade) values('ACIT4620', 0)")
    cursor.execute("insert into grades(course, grade) values('ACIT4850', 0)")
    cursor.execute("insert into grades(course, grade) values('ACIT4880', 0)")
    cursor.execute("insert into grades(course, grade) values('ACIT4900', 0)")
    mydb.commit()
except mysql.connector.errors.ProgrammingError:
    pass

auth_cursor = auth_db.cursor()
auth_cursor.execute("SHOW TABLES")
for x in auth_cursor:
    pass

try:
    auth_cursor.execute(''' 
                CREATE TABLE users (
                username VARCHAR(45) NOT NULL,
                password VARCHAR(45) NOT NULL
                );
            ''')            
    auth_db.commit()
except mysql.connector.errors.ProgrammingError:
    pass


@app.route('/', methods=['GET'])
def data_entry():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM grades")
    data = cursor.fetchall()

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
        cursor = mydb.cursor()
        #query="insert into grades(course, grade) values(%s,%s)"            # insert query
        query="update grades set course = %s, grade = %s where id = %s"     # update query

        id = 1
        for item in grades_list.items():
            #cur.execute(query, (item[0],item[1]))       # inserts into db
            cursor.execute(query, (item[0],item[1],id))    # alters existing entries
            mydb.commit()
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
    app.run(debug=True, host='0.0.0.0', port=5000)