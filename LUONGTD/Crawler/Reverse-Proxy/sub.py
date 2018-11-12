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

data = {}
###Detect functions
def find(data):
    for keyword, description in CDN.items():        
        if re.findall(keyword.lower(), data) != []:
            return description
    return -1

def Whois2(url, result):
    hostname = url.split('www.')[1]
    out1 = commands.getoutput("host " + hostname)
    if out1 != '':
        regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
        addresses = regexp.finditer(out1)
        for addr in addresses:  
            out2 = commands.getoutput("whois " + addr.group())
            x = find(out2.lower())
            if x != -1:
                if x not in result:
                    result.append(x)
    else:
        hostname = urlparse.urlparse(url).netloc
        out1 = commands.getoutput("host " + hostname)
        if out1 != '':
            regexp = re.compile('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b')
            addresses = regexp.finditer(out1)
            for addr in addresses:  
                #print(addr.group())
                out2 = commands.getoutput("whois " + addr.group())
                x = find(out2.lower())
                if x != -1:
                    if x not in result:
                        result.append(x)
    return result


## Main:
hostname = "http://vtv.vn"
req = requests.get(hostname, timeout=3)
print(req.headers)