import threading
import Queue
import csv	
import requests
import sqlite3
import ssl
from detection import *

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE	

url = "apple.com"

hurl = "http://" + url
print(hurl)
try:		
	req = requests.get(hurl, timeout=3)
	try:
		wsv = req.headers
		print(wsv)
		#ap = check_header(wsv, apps)
		#print(ap)
		#if data.get(ap) != None:
		#	data[ap] = data[ap] + 1
		#else:
		#	data[ap] = 1
	except:
		print("Unable to retrive server information from request.headers")
except:
	print("Site is unreachable. Too bad!!")
