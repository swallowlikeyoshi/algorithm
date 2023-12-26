from flask import session
from flask_socketio import emit, join_room, leave_room, Namespace
from datetime import datetime
from todaysUnyang import chatting_DB

class Chat(Namespace):

    def _get_session_info():
        session['datetime'] = datetime.now()
        session_info = dict()
        data_list = { 'name', 'room', 'datetime', 'headers' }
        for name in data_list:
            session_info[name] = str(session.get(name, ''))
        return session_info

    def on_connect(self):
        session_info = Chat._get_session_info()
        chatting_DB.users(session_info, is_online = True)
        pass

    def on_disconnect(self):
        session_info = Chat._get_session_info()
        chatting_DB.users(session_info, is_online = False)
        pass

    def on_joined(self, *asdf):
        session_info = Chat._get_session_info()
        join_room(session_info['room'])
        to_client = {
            'sent_message': '\t<' + str(session.get('name')) + '>: 입장'
        }
        emit('status', to_client, room = session_info['room'])

    def on_text(self, data):
        session_info = Chat._get_session_info()
        print('' + str(session_info['name']) + ': ' + data['message'])
        to_client = {
            'session_name': session_info['name'],
            'session_room': session_info['room'],
            'datetime': session_info['datetime'],
            'sent_message': str(data['message'])
        }
        emit('message', to_client, room = session_info['room'])
        chatting_DB.texts(session_info, data['message'])

    def on_left(self, data):
        session_info = Chat._get_session_info()
        leave_room(session_info['room'])
        to_client = {
            'sent_message': '\t<' + str(session.get('name')) + '> 퇴장'
        }
        emit('status', to_client, room = session_info['room'])