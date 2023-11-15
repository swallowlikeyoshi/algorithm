import sqlite3

print("찾을 이름 입력: ")
user_name = input()

conn = sqlite3.connect('chatting_DB.db')
cur = conn.cursor()
cur.execute('SELECT * FROM logs WHERE name = "' + user_name + '"')

print('--------------logs----------------')
for i in cur.fetchall():
    print(i[0], i[2], i[3], i[4])
print('----------------------------------')