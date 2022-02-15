from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

with open('mysql.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())
    app.config['MYSQL_USER'] = app_config['datastore']['user']
    app.config['MYSQL_PASSWORD'] = app_config['datastore']['password']
    app.config['MYSQL_DB'] = app_config['datastore']['db']
    app.config['MYSQL_HOST'] = app_config['datastore']['hostname']
    mysql = MySQL(app)


@app.route('/', methods=['GET'])
def my_form():
    cur = mysql.connection.cursor()            # updates default values
    cur.execute("SELECT * FROM grades")
    data = cur.fetchall()

    return render_template('home.html', data=data)

@app.route('/', methods=['POST'])
def my_form_post():
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
                return redirect(url_for("my_form"))
        elif grade == "":
            break
        else:
            flash("❌⚠️ Grades should be numeric values")
            return redirect(url_for("my_form"))

    
    if len(grades_list) != 7:
            flash("❌⚠️ Please enter a grade for all courses")
            return redirect(url_for("my_form"))

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
        return redirect(url_for("my_form"))
        #return render_template('home.html')


    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)