import sqlite3

conn = sqlite3.connect('id2.db', check_same_thread=False)

cursor = conn.cursor()

cursor.execute('''SELECT user_id FROM USER_TABLE''')
if cursor.fetchone() is None:
    print('DB IS EMPTY')
else:
    for value in cursor.execute('SELECT user_id FROM USER_TABLE'):
        print(value[0])



