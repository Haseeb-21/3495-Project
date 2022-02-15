import mysql.connector
import yaml

with open('mysql.yml', 'r') as f: 
  app_config = yaml.safe_load(f.read())
  mydb = mysql.connector.connect(
  host=app_config['datastore']['hostname'],
  user=app_config['datastore']['user'],
  password=app_config['datastore']['password'],
  database=app_config['datastore']['db']
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM grades")
result = mycursor.fetchall()

i = 0
grades = []
for entry in result:
    grades.append(entry[2])

# Get statistics
min = min(grades)
max = max(grades)
avg = sum(grades) / len(grades)



