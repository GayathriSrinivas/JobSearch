#! /usr/bin/python

import psycopg2
import traceback
import json
import sys
from os import listdir
from os.path import isfile, join

fp = open('dbDetails.txt','r')
db_string = fp.read().strip()
fp.close()
N = 42582

def company_and_roles():
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    mypath = "company1/" 
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for filename in onlyfiles:
        try:
            data = json.load(open('company1/%(filename)s' % locals(), 'r'))
            if data and data.has_key('meta') and data['meta'].has_key('name'):
                name = data['meta']['name']
                revenue = data['meta'].get('Revenue', None)
                website = data['meta'].get('website', None)
                location = data['meta'].get('location', None)
                c_type = data['meta'].get('Type', None)
                size = data['meta'].get('12', [None])
                size = size[-1] if len(size) > 0 else None
                revenue = data['meta'].get('Revenue', None)
                industry = data['meta'].get('Industry', None)
                ceo = None
                ceo_picture = None
                if data.has_key('ceo'):
                    ceo = data['ceo'].get('name', None)
                    ceo_picture = data['ceo'].get('avatar', None)
                rating = None
                if data.has_key('satisfaction') and data['satisfaction'].has_key('ratings'):
                    rating = data['satisfaction']['ratings']
                # check if already exists
                q = "SELECT COUNT(1) FROM g_company WHERE company_name=%s"
                cur.execute(q, (name, ))
                count = cur.fetchone()[0]
                if count == 1:
                    print >> sys.stderr, 'Update file : %(filename)s %(name)s' % locals()
                    q = "UPDATE g_company set revenue=%s,location=%s,ceo=%s,rating=%s,type=%s,size=%s,website=%s,ceo_picture=%s,industry=%s where company_name=%s"
                    cur.execute(q, (revenue, location, ceo, rating, c_type, size, website, ceo_picture, industry,name))
                elif count == 0:
                    print >> sys.stderr, 'Update file : %(filename)s %(name)s' % locals()
                    q = "INSERT INTO g_company (company_name, revenue, location, ceo, rating, type, size, website, ceo_picture, industry) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cur.execute(q, (name, revenue, location, ceo, rating, c_type, size, website, ceo_picture, industry))

            if data and data.has_key('salary') and data['salary']:
                for entry in data['salary']:
                    if not entry.has_key('position'):
                        continue
                    q = "SELECT COUNT(1) FROM g_role WHERE role_name=%s"
                    cur.execute(q, (entry['position'], ))
                    count = cur.fetchone()[0]
                    if count == 0:
                        q = "INSERT INTO g_role (role_name) VALUES (%s)"
                        cur.execute(q, (entry['position'], ))
            conn.commit()
        except:
            print >> sys.stderr, 'failed for %(filename)s' % locals()
            traceback.print_exc()
        else:
            print >> sys.stderr, 'done with %(filename)s' % locals()
    cur.close()
    conn.close()

def related_company():
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    mypath = "company1"
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for filename in onlyfiles:
        try:
            data = json.load(open('company1/%(filename)s' % locals(), 'r'))
            #Populate g_related_company table
            if data and data.has_key('meta') and data['meta'].has_key('Competitors'):
                q = "SELECT company_id from g_company where company_name=%s"
                cur.execute(q, (data['meta']['name'], ))
                id1 = cur.fetchone()[0]
                for company in data['meta']['Competitors'].split(','):
                    q = "SELECT count(1) from g_company where company_name=%s"
                    cur.execute(q, (company, ))
                    count = cur.fetchone()[0]
                    if count == 0:
                        q = "INSERT into g_company (company_name) VALUES (%s) returning company_id"
                    else:
                        q = "SELECT company_id from g_company where company_name=%s"
                    cur.execute(q, (company, ))
                    id2 = cur.fetchone()[0]
                    q = "INSERT into g_related_company (company_id1,company_id2) VALUES (%s,%s)"
                    cur.execute(q, (id1,id2))
                conn.commit()
            #Populate g_salary table
            if data and data.has_key('salary') and data['salary'] and data.has_key('meta') and data['meta'].has_key('name') and data['meta']['name']:
                name = data['meta']['name']
                q = "SELECT company_id from g_company where company_name=%s"
                cur.execute(q, ( data['meta']['name'], ))
                company_id = cur.fetchone()[0]
                for salary in data['salary']:
                    if not salary.has_key('position'):
                        continue
                    mean = salary.get('mean',None)
                    range_sal = salary.get('range',None)
                    range_low = range_sal[0] if len(range_sal) > 1 else None
                    range_high = range_sal[1] if len(range_sal) > 1 else None
                    samples = salary.get('samples',None)
                    q = "SELECT role_id from g_role where role_name=%s"
                    cur.execute(q, (salary['position'], ))
                    role_id = cur.fetchone()[0]
                    q = "INSERT into g_salary (company_id,role_id,mean,range_low,range_high,samples) VALUES (%s,%s,%s,%s,%s,%s)"
                    cur.execute(q,(company_id,role_id,mean,range_low,range_high,samples))
                conn.commit()
        except:
            print >> sys.stderr, 'failed for %(filename)s %(name)s' % locals()
            traceback.print_exc()
        else:
            print >> sys.stderr, 'done with %(filename)s %(name)s' % locals()
    cur.close()
    conn.close()

if __name__ == "__main__":
    company_and_roles()
    related_company()