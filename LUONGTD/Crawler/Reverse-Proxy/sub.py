#!/usr/bin/env python

from __future__ import print_function
import argparse
import signal
import sys
from Detection import *
import pandas as pd
import csv
import threading
import Queue
import operator

if sys.version_info >= (3, 0):
    import urllib.parse as urlparse
else:
    import urlparse



## Defines
NUM_SPIDERS = 50
q = Queue.Queue()
urls = []
data = {}
Do_not_use = 0
### read top-1m urls
with open('top-1m.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    i = 0
    for line in csv_reader:
        i = i + 1
        url = line[1]
        urls.append(url)
        #if i == 100000:
        #   break

def sanitizeURL(hostname):
    components = urlparse.urlparse(hostname)
    #print(components)
    hostname = "http://www." + hostname if components.scheme == '' else hostname
    return hostname

### Functions
url = "panda.tv"
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

print(data)

