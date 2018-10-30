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
from bs4 import BeautifulSoup
import ast
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def sanitizeURL(hostname):
    components = urlparse.urlparse(hostname)
    hostname = "http://" + hostname if components.scheme == '' else hostname
    return hostname


url = "dosarrest.com"
#"pokemon.com" 
hostname = sanitizeURL(url)
print(hostname)
hostname = urlparse.urlparse(hostname).netloc
print(hostname)
out = commands.getoutput("host " + url)
print(out)
regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
print(regexp)
addresses = regexp.finditer(out)    
print(addresses)
for addr in addresses:
    x = addr.group()
    print(x)
    hostname = "https://ipinfo.io/" + x
    #url = "https://ipinfo.io/220.242.131.60"
    print(hostname)
    req = requests.get(hostname)
    soup = BeautifulSoup(req.text, "lxml")
    tag = soup.p.string
    dic =   ast.literal_eval(tag)
    print(dic["org"])


"""

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

"""
