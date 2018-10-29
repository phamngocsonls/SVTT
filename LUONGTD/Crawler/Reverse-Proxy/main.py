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


## Defines
NUM_SPIDERS = 50
q = Queue.Queue()
urls = []
data = {}
company = {}
Do_not_use = 0

### read top-1m urls
with open('top-1m.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    i = 0
    for line in csv_reader:
        i = i + 1
        url = line[1]
        urls.append(url)
        #if i == 1000:
        #   break

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
    ans = -1
    dns = DNS_detect(hostname)
    if dns != -1:
        ans = dns
    else:    
        cdn = HTTP_detect(hostname)
        if cdn != -1:
            ans = cdn
        else:    
            subdomain = Subdomain_detect(hostname)
            if subdomain != -1:
                ans = subdomain
            else:
                whois = Whois_detect(hostname)
                if whois != -1:
                    ans = whois
                else:
                    err = ErrorServer_detect(hostname)
                    if err != -1:
                        ans = err

    if ans == -1:
        print("No Reverse Proxy!!")
    else:
        if ans != None:             
            if data.get(ans) != None:
                data[ans] = data[ans] + 1
            else:
                data[ans] = 1
            print(ans)
            company[url] = ans


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