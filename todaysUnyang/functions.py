from flask import render_template, request
from datetime import datetime
from todaysUnyang import app
from todaysUnyang import mealServiceDietInfo as meal
from todaysUnyang import 시간표_수정본 as timeTable



# HTML 페이지 반환용 함수

@app.route('/')
def index():
    return render_template('index.html', dietInfo = meal.getDietInfo(_today()))

@app.route('/developers')
def developers():
    return render_template('Developers.html')

@app.route('/moreinfo')
def moreinfo():
    return render_template('Moreinfo.html')

@app.route('/making')
def making():
    return render_template('Making.html')



# HTMX 요청 처리용 함수

@app.route('/_timetable', methods = ['GET', 'POST'])
def _get_timetable():
    result = request.form
    time_info = timeTable.get_time_table(result['grade'], result['class'], result['semester'], _today())
    return time_info



# 내부 사용용 함수

def _today():
    return str(datetime.date(datetime.today())).replace('-', '')