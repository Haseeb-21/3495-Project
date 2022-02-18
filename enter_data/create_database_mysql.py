import mysql.connector 
 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Haseeb-2001"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE grades")

db_conn = mysql.connector.connect(host="localhost", user="root", 
password="Haseeb-2001", database="grades") 
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute(''' 
          CREATE TABLE grades (
          id INT NOT NULL AUTO_INCREMENT,
          course VARCHAR(45) NOT NULL,
          grade INT NOT NULL,
          PRIMARY KEY (id));
          ''')

db_cursor.execute("insert into grades(course, grade) values('ACIT3495', 0)")
db_cursor.execute("insert into grades(course, grade) values('ACIT3855', 0)")
db_cursor.execute("insert into grades(course, grade) values('ACIT4640', 0)")
db_cursor.execute("insert into grades(course, grade) values('ACIT4620', 0)")
db_cursor.execute("insert into grades(course, grade) values('ACIT4850', 0)")
db_cursor.execute("insert into grades(course, grade) values('ACIT4880', 0)")
db_cursor.execute("insert into grades(course, grade) values('ACIT4900', 0)")
 
db_conn.commit() 
db_conn.close() 