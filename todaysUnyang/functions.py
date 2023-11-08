from flask import Flask, render_template
from datetime import datetime
from todaysUnyang import app
import mealServiceDietInfo as meal

@app.route('/')
def index():
    return render_template('index.html', dietInfo = meal.getDietInfo(today()), calrorieInfo = meal.getCalorieInfo(today()))

@app.route('/Developers')
def get_developers_info():
    return render_template('Developers.html')

def today():
    return str(datetime.date(datetime.today())).replace('-', '')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
