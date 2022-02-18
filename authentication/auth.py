import csv
import sys, os

FILE = os.path.abspath('../authentication/auth.csv')


def check_auth(user, password):
    auth_pair = [user, password]

    # checks user and password with auth service 
    with open(FILE, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if auth_pair == row:
                return True

def add_user(user, password):
    with open(FILE, 'r') as f:
        # checks if username already exists
        row = [user, password]
        csvreader = csv.reader(f)
        
        for row in csvreader:
            if user == row[0]:
                return False

    with open(FILE, 'a', newline='') as f:
        # adds new user
        writer = csv.writer(f)
        row = (user, password)
        print(row)
        writer.writerow(row)
        return True
