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
import re
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


url = "http://www.Tianjinecocity.gov.sg"
hostname = url
result = []
result = HTTP_detect(hostname, result)   
result = DNS_detect(hostname, result)   
result = Subdomain_detect(hostname, result)
result = Whois_detect(hostname, result)
if result == []:
    print("No Reverse Proxy!!")
print(result)


"""
            whois = Whois_detect(hostname)
            if whois != -1:
                ans = whois
            else:
                err = ErrorServer_detect(hostname)
                if err != -1:
                    ans = err

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
"""