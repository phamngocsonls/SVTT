import threading
import Queue
import csv	
import requests
import pandas as pd

# Ignore SSL certificate errors

urls = []
### read top-1m urls
with open('top-1m.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    i = 0
    for line in csv_reader:
        i = i + 1
        if i > 500000:
           urls.append(line[1])

print(urls)

hf =pd.DataFrame(urls, columns=['site'])
hf.to_csv('top-500k2.csv', encoding='utf-8')
