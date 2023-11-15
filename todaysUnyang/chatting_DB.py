import sqlite3
from todaysUnyang import BASE_DIR

def push_log(session_info, type, contents):
    match type:
        case 'text':
            push_text_log(session_info, contents)
        case 'user':
            push_user_log(session_info, contents)
        case _:
            raise

def push_text_log(session_info, message):
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    data = (session_info['name'], session_info['room'], session_info['datetime'], 'message', message, session_info['headers'])
    cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", data)
    connection.commit()
    cur.close()
    connection.close()
    return

def push_user_log(session_info, is_online):
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    data = (session_info['name'], session_info['room'], session_info['datetime'], 'is_online', 'online' if is_online == True else 'offline', session_info['headers'])
    cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)", data)
    connection.commit()
    connection.close()
    return

DB_PATH = BASE_DIR + '\\resources' + '\\chatting_DB.db'


try:
    f = open(DB_PATH, 'r')
except:
    f = open(DB_PATH, 'w')
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS logs (name text, room text, datetime DATETIME, type text, contents text, headers text)")
    connection.commit()
    cur.close()
    connection.close()
finally:
    f.close()

if __name__ == '__main__':
    connection = sqlite3.connect(DB_PATH)
    cur = connection.cursor()

    cur.execute("SELECT * FROM logs")
    for i in cur.fetchall():
        print(i[0], i[2], i[4])

    connection.commit()
    cur.close()
    connection.close()