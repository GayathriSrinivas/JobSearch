#! /usr/bin/python

import csv
import random
import requests
import traceback
import urllib
import sys

if len(sys.argv) != 3:
    print "Usage: %s <start_row> <end_row>" % sys.argv[0]
    sys.exit(0)

start = int(sys.argv[1])
end = int(sys.argv[2])

url = "http://open.dapper.net/transform.php?dappName=linked_in_scraper&transformer=JSON&applyToUrl=%s"

reader = csv.reader(open('linked_in_profiles2.csv', 'rb'))
i = 0
for row in reader:
    i += 1
    if i - 1 < start:
        continue
    if i - 1 > end and end != -1:
        continue
    try:
        print 'Processing %d - %s' % (i, row[0].decode('utf-8'))    
    except:
        pass
    try:
        data = requests.get(url % urllib.quote(row[1]))
        f = open('data/%(i)d.json' % locals(), 'w')
        f.write(data.content)
        f.close()
    except:
        print 'failed'
        print traceback.format_exc()

print 'done :)'
