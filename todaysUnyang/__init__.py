from flask import Flask
from flask_socketio import SocketIO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

socket_io = SocketIO(logger = False, engineio_logger = False, cors_allowed_origins = '*')

def create_app(is_debug = False):
    app = Flask(__name__)
    app.debug = is_debug
    app.config['SECRET_KEY'] = '😍😍😍😍😍'

    socket_io.init_app(app)

    from todaysUnyang.chatting_events import Chat
    socket_io.on_namespace(Chat('/chatting'))

    # 채팅 HTTP 응답 가져오기
    from todaysUnyang.chatting_routes import chatting
    app.register_blueprint(chatting)

    # 오늘의 운양고 HTTP 가져오기
    
    from todaysUnyang.todaysUnyang_routes import todaysUnyang
    app.register_blueprint(todaysUnyang)

    return app