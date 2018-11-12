from __future__ import print_function
import pandas as pd
import csv
import operator


data = {}
TOTAL_SITES_FOUND = float(float(56664) + float(91762))
print(TOTAL_SITES_FOUND)

with open('result1.csv', 'r') as csv_file1:
    csv_reader1 = csv.reader(csv_file1)
    for line in csv_reader1:
        site = line[1]
        num = int(line[2])
        if data.get(site) == None:
        	data[site] = num
        else:
        	data[site] += num

with open('result2.csv', 'r') as csv_file2:
    csv_reader2 = csv.reader(csv_file2)
    for line in csv_reader2:
        site = line[1]
        num = int(line[2])
        if data.get(site) == None:
        	data[site] = num
        else:
        	data[site] += num

sorted_data2 = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_data2)

df = pd.DataFrame(sorted_data2, columns=['Reverse-Proxy-Services', 'Sites'])
df.to_csv('TOTAL-NUM.csv', encoding = 'utf-8')

data1 = {}
for site, num in data.iteritems():
	num = 100*float(num)/TOTAL_SITES_FOUND
	data1[site] = float("%0.2f"%num)
	print (data1[site])

sorted_data1 = sorted(data1.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_data1)
df = pd.DataFrame(sorted_data1, columns=['Reverse-Proxy-Services', 'Market-Share'])
df.to_csv('RESULT.csv', encoding = 'utf-8')