import threading
import Queue
import csv	
import requests
import sqlite3
import ssl
from detection import *

urls =[]

with open('top-1m.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	i = 0
	for line in csv_reader:
		i = i + 1
		url = line[1]
		urls.append(url)
		if i == 100000:
			break

print(len(urls))
print(urls)