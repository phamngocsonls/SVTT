import csv	
import requests
import sqlite3
import ssl
from detection import *

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE	

### SQLite
conn = sqlite3.connect('spider.splite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS WebServer
	(app TEXT UNIQUE, num INTEGER)''')

## read urls
urls = []
with open('top-1k.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	for line in csv_reader:
		url = line[1]
		urls.append(url)

### Read json file
apps = read_clues()

### Main
i = 0
for url in urls:
	i = i + 1
	hurl = "http://" + url
	print("{}: {}".format(i, hurl))
	try:		
		req = requests.get(hurl, timeout=3)
		try:
			wsv = req.headers['server']
			ap = check_header(wsv, apps)
			cur.execute('INSERT OR IGNORE INTO WebServer (app, num) VALUES (?, ?)', (ap, 1))
			cur.execute('UPDATE WebServer SET num = num + 1 WHERE app = ?', (ap,))
			print(ap)
		except:
			print("Unable to retrive server information from request.headers")
			continue
	except:
		print("Site is unreachable. Too bad!!")

conn.commit()



## Issues:
"""
1. Mot so websites trong list khong truy cap duoc
2. Mot so websites HTTP response khong co thong tin webserver
3. Too Slow
"""
