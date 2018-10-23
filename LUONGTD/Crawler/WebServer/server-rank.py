import sqlite3

conn = sqlite3.connect('test.splite')
cur = conn.cursor()

cur.execute('SELECT * FROM WebServer ORDER BY num DESC')
conn.commit()