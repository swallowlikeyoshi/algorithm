from flask import session
from flask_socketio import emit, join_room, leave_room, Namespace
from datetime import datetime
from todaysUnyang import chatting_DB, chatting_safe

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
        chatting_DB.push_log(session_info, type = 'user', contents = True)
        pass

    def on_disconnect(self):
        session_info = Chat._get_session_info()
        chatting_DB.push_log(session_info, type = 'user', contents = False)
        pass

    def on_joined(self, *asdf):
        session_info = Chat._get_session_info()
        join_room(session_info['room'])
        # to_client = {
        #     'sent_message': '<' + str(session.get('name')) + '>: 입장'
        # }

        to_client = {
            'name': session_info['name'],
            'room': session_info['room'],
            'datetime': session_info['datetime'],
            'type': 'user',
            'contents': True
        }

        emit('status', to_client, room = session_info['room'])

    def on_text(self, data):
        session_info = Chat._get_session_info()
        print('<' + str(session_info['name']) + '>: ' + data['message'])

        if not chatting_safe.is_safe_text(data['message']):
            message = '***'
        else:
            message = data['message']

        to_client = {
            'name': session_info['name'],
            'room': session_info['room'],
            'datetime': session_info['datetime'],
            'type': 'text',
            'contents': message
        }

        emit('message', to_client, room = session_info['room'])
        chatting_DB.push_log(session_info, type = 'text', contents = data['message'])

    def on_left(self, data):
        session_info = Chat._get_session_info()
        leave_room(session_info['room'])
        # to_client = {
        #     'sent_message': '<' + str(session.get('name')) + '> 퇴장'
        # }

        to_client = {
            'name': session_info['name'],
            'room': session_info['room'],
            'datetime': session_info['datetime'],
            'type': 'user',
            'contents': False
        }

        emit('status', to_client, room = session_info['room'])