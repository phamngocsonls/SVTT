#!/usr/bin/env python

from __future__ import print_function
from Detection import *
import pandas as pd
import csv
import threading
import operator

if sys.version_info >= (3, 0):
    import urllib.parse as urlparse
    import queue as Queue
else:
    import urlparse
    import Queue

import sqlite3
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

## SQLite
conn = sqlite3.connect('report.sqlite', check_same_thread=False)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ReverseProxy
    (Provider TEXT UNIQUE, Num INTEGER)''')
cur.close()

## Defines
NUM_SPIDERS = 50
q = Queue.Queue()
urls = []
data = {}
company = {}
Do_not_use = 0

### read top-1m urls
with open('top-500k2.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    i = 0
    for line in csv_reader:
        i = i + 1
        url = line[1]
        urls.append(url)
        if i == 10000:
           break

def sanitizeURL(hostname):
    components = urlparse.urlparse(hostname)
    #print(components)
    hostname = "http://www." + hostname if components.scheme == '' else hostname
    return hostname

### Functions
def create_jobs():
    for url in urls:
        q.put(url)
    q.join()

# crawl the next url
def work():
    while True:
        url = q.get()
        spider(url)
        q.task_done()

# Create spider threads (will be terminated when main exits)
def create_spiders():
    for x in range(NUM_SPIDERS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Spider definition
def spider(url):
    hostname = sanitizeURL(url)
    result = []
    result = HTTP_detect(hostname, result)
    result = DNS_detect(hostname, result)  
    result = Subdomain_detect(hostname, result)
    result = Whois_detect(hostname, result)
    if result == []:
        print("No Reverse Proxy!!")
    else:
        for an in result:
            if an != None:
                company[url] = []     
                cur = conn.cursor()        
                if data.get(an) == None:
                    data[an] = 1
                    try:
                        cur.execute('INSERT OR IGNORE INTO ReverseProxy (Provider, Num) VALUES (?, ?)', (an, 1))
                    except:
                        print("{}-> SQLite: <INSERT> Operation error!!".format(an))
                else:
                    data[an] = data[an] + 1
                    try:
                        cur.execute('UPDATE ReverseProxy SET Num=Num+1 WHERE Provider=?',(an, ))
                    except:
                        print("{}-> SQLite: <UPDATE> Operation error!!".format(an))
                print(an)
                company[url].append(an)
                try:
                    conn.commit()
                except:
                    print("{}-> SQLite: Nothing to commit".format(an))
                #conn.commit()
                cur.close()

### Main
create_spiders()
create_jobs()


### Evaluation:
print("\n\nEVALUATION:")
count = 0
for key, value in data.iteritems():
    count = count + value

print("\nTOTAL SITES:  {}".format(count))
#print(company)
sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
#print(sorted_data.reverse())

df = pd.DataFrame(sorted_data, columns=['Reverse-Proxy-Services', 'Sites'])
df.to_csv('result.csv', encoding = 'utf-8')

companies = []

for key, value in company.iteritems():
    temp = [key, value]
    companies.append(temp)

hf = pd.DataFrame(companies, columns=['websites', 'CDN'])
hf.to_csv('companies.csv', encoding = 'utf-8')

