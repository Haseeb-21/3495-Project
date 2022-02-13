from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Haseeb-2001'
app.config['MYSQL_DB'] = 'grades'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def my_form():
    cur = mysql.connection.cursor()            # updates default values
    cur.execute("SELECT * FROM grades")
    data = cur.fetchall()

    return render_template('home.html', data=data)

@app.route('/', methods=['POST'])
def my_form_post():
    print("POOOOOOOST")
    grades_list = {}
    i = 1

    while i <= 7:
        course = request.form[f"course{i}"]
        grade = request.form[f"grade{i}"]
        if grade.isdigit():
            grades_list[course] = float(grade)
            i += 1
        elif grade == "":
            break
        else:
            flash("Grades should be numeric values")
            return redirect(url_for("my_form"))

    
    if len(grades_list) != 7:
            flash("Please enter a grade for all courses")
            return redirect(url_for("my_form"))
            #return render_template('home.html')
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

        flash("Grades added successfully")
        return redirect(url_for("my_form"))
        #return render_template('home.html')


    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    #app.config['SESSION_TYPE']