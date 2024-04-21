import sqlite3

conn = sqlite3.connect('education.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM sqlite_sequence;')

rows = cursor.fetchall()
print(rows)