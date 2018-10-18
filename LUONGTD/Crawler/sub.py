import httplib2
import csv	
"""
This script downloads the alexa top 1M sites, unzips it, and reads the CSV and
returns a list of the top N sites.
"""

import zipfile
from io import StringIO
from urllib.request import urlopen

ALEXA_DATA_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'


def alexa_etl():
    """
    Generator that:
        Extracts by downloading the csv.zip, unzipping.
        Transforms the data into python via CSV lib
        Loads it to the end user as a python list
    """

    f = urlopen(ALEXA_DATA_URL)
    buf = StringIO.StringIO(f.read())
    zfile = zipfile.ZipFile(buf)
    buf = StringIO.StringIO(zfile.read('top-1m.csv'))
    for line in buf:
        (rank, domain) = line.split(',')
        yield (int(rank), domain.strip())


def top_list(num=100):
    a = alexa_etl()
    return [next(a) for x in range(num)]


if __name__ == "__main__":
    print (top_list())


h = httplib2.Http()
resp, content = h.request("https://uet.vnu.edu.vn/", "GET")

print(resp)
x = resp['server']
#print(x)
alexa.top_list(20)
