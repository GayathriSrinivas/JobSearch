#! /usr/bin/python

import csv
import random
import requests
import traceback

search_param="%s-%d-%d-%d"

url = "http://open.dapper.net/transform.php?dappName=linkedin_profiles&transformer=JSON&v_q=%s"

f = open('linked_in_profiles2.csv', 'a')
writer = csv.writer(f)
letters = map(chr, range(ord('k'), ord('z') + 1))
numbers = []
for i in range(1,20):
    for j in range(1, 20):
        for k in range(1, 20):
            numbers.append((i, j, k))
random.shuffle(numbers)
random.shuffle(letters)
for letter in letters:
    for num in numbers:
        search_param_str = search_param % (letter, num[0], num[1], num[2])
        try:
            dapp_url = url % search_param_str
            print 'Fetching url ', dapp_url
            people = requests.get(dapp_url).json()['fields']['people']
            print 'Fetched, Processing'
            for person in people:
                print 'Processing ', person['value'].encode('utf-8')
                try:
                    writer.writerow((person['value'].encode('utf-8'), person['href']))
                except:
                    print "failed"
                    print traceback.print_exc()
        except:
            print "failed"
            print traceback.print_exc()
f.close()
