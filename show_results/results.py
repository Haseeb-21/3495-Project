from flask import Flask, request, render_template, url_for, redirect, flash
from flask_pymongo import PyMongo

app = Flask(__name__)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/analytics"
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def get_results():
    results = mongo.db.analytics.find_one_or_404({"id": 1})
    min = results['min']
    max = results['max']
    mean = results['mean']

    return render_template('results.html', min=min, max=max, mean=mean)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)