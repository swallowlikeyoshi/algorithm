from flask import Flask, render_template
from datetime import datetime
from todaysUnyang import app
from todaysUnyang import mealServiceDietInfo as meal

@app.route('/')
def index():
    return render_template('index.html', dietInfo = meal.getDietInfo(today()), calrorieInfo = meal.getCalorieInfo(today()))

@app.route('/developers')
def developers():
    return render_template('Developers.html')

@app.route('/moreinfo')
def moreinfo():
    return render_template('Moreinfo.html')

@app.route('/making')
def making():
    return render_template('Making.html')

def today():
    return str(datetime.date(datetime.today())).replace('-', '')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
