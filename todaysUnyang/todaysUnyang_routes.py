from flask import render_template, request, Blueprint, send_from_directory
from datetime import datetime
from todaysUnyang import mealServiceDietInfo as meal
from todaysUnyang import 시간표_수정본 as timeTable
from todaysUnyang import 날씨정보알림 as weather
from todaysUnyang import BASE_DIR

todaysUnyang = Blueprint('todaysUnyang', __name__)

# 특수 기능용 함수
@todaysUnyang.route('/robots.txt')
def robots():
    return send_from_directory(BASE_DIR, request.path[1:])

# HTML 페이지 반환용 함수
@todaysUnyang.route('/')
def index():
    return render_template('index.html', diet_info = meal.get_diet_info(_today()), weather_info = weather.get_weather_info())

@todaysUnyang.route('/developers')
def developers():
    return render_template('Developers.html')

@todaysUnyang.route('/moreinfo')
def moreinfo():
    return render_template('Moreinfo.html')

@todaysUnyang.route('/making')
def making():
    return render_template('Making.html')



# HTMX 요청 처리용 함수

@todaysUnyang.route('/_timetable', methods = ['GET', 'POST'])
def _get_timetable():
    result = request.form
    time_info = timeTable.get_time_table(result['grade'], result['class'], result['semester'], _today())
    return time_info



# 내부 사용용 함수

def _today():
    return str(datetime.date(datetime.today())).replace('-', '')