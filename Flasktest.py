from flask import Flask, render_template
from datetime import datetime
import mealServiceDietInfo as meal

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html', lunch = getMealDietInfoToday())

@app.route('/getlunch')
def getMealDietInfoToday():
    today = str(datetime.date(datetime.today())).replace('-', '')
    return meal.getDietInfo(today)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
