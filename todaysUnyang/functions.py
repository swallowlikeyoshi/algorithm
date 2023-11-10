from flask import Flask, render_template, request
from datetime import datetime
from todaysUnyang import app
from todaysUnyang import mealServiceDietInfo as meal
from todaysUnyang import 시간표_수정본 as timeTable

@app.route('/')
def index():
    return render_template('index.html', dietInfo = meal.getDietInfo(today()))

@app.route('/developers')
def developers():
    return render_template('Developers.html')

@app.route('/moreinfo')
def moreinfo():
    return render_template('Moreinfo.html')

@app.route('/making')
def making():
    return render_template('Making.html')

@app.route('/_timetable', methods = ['GET', 'POST'])
def get_timetable():
    result = request.form
    time_info = timeTable.get_time_table(result['grade'], result['class'], result['semester'], today())
    return time_info

def today():
    return str(datetime.date(datetime.today())).replace('-', '')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
