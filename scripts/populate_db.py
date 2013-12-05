#! /usr/bin/python

import psycopg2
import traceback
import json
import sys


fp = open('dbDetails.txt','r')
db_string = fp.read().strip()
fp.close()

N = 42582

def skills():
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    for i in range(N):
        try:
            data = json.load(open('data/%(i)d.json' % locals(), 'r'))
            if data and data.has_key('fields') and data['fields'].has_key('skills'):
                for skill in data['fields']['skills']:
                    q = "SELECT COUNT(1) FROM skill WHERE skill_name=%s"
                    cur.execute(q, (skill['value'], ))
                    count = cur.fetchone()[0]
                    if count == 0:
                        q = "INSERT INTO skill (skill_name) VALUES (%s)"
                        cur.execute(q, (skill['value'], ))
                conn.commit()
        except:
            print >> sys.stderr, 'failed for %(i)d.json' % locals()
            traceback.print_exc()
        else:
            print >> sys.stderr, 'done with %(i)d.json' % locals()
    cur.close()
    conn.close()

def companies_and_roles():
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    for i in range(N):
        try:
            data = json.load(open('data/%(i)d.json' % locals(), 'r'))
            if data and data.has_key('groups') and data['groups'].has_key('positions'):
                for position in data['groups']['positions']:
                    if position.has_key('company'):
                        q = "SELECT COUNT(1) FROM company WHERE company_name=%s"
                        cur.execute(q, (position['company'][0]['value'], ))
                        count = cur.fetchone()[0]
                        if count == 0:
                            q = "INSERT INTO company (company_name) VALUES (%s)"
                            cur.execute(q, (position['company'][0]['value'], ))
                    if position.has_key('role'):
                        q = "SELECT COUNT(1) FROM role WHERE role_name=%s"
                        cur.execute(q, (position['role'][0]['value'], ))
                        count = cur.fetchone()[0]
                        if count == 0:
                            q = "INSERT INTO role (role_name) VALUES (%s)"
                            cur.execute(q, (position['role'][0]['value'], ))
                conn.commit()
            elif data and data.has_key('fields') and data['fields'].has_key('title'):
                tparts = data['fields']['title'][0]['value'].split(' at ')
                if len(tparts) > 1:
                    role = tparts[0].strip()
                    company = tparts[1].strip()
                    q = "SELECT COUNT(1) FROM company WHERE company_name=%s"
                    cur.execute(q, (company, ))
                    count = cur.fetchone()[0]
                    if count == 0:
                        q = "INSERT INTO company (company_name) VALUES (%s)"
                        cur.execute(q, (company, ))
                    q = "SELECT COUNT(1) FROM role WHERE role_name=%s"
                    cur.execute(q, (role, ))
                    count = cur.fetchone()[0]
                    if count == 0:
                        q = "INSERT INTO role (role_name) VALUES (%s)"
                        cur.execute(q, (role, ))
                conn.commit()
        except:
            print >> sys.stderr, 'failed for %(i)d.json' % locals()
            traceback.print_exc()
        else:
            print >> sys.stderr, 'done with %(i)d.json' % locals()
    cur.close()
    conn.close()

def person_skills_and_jobs():
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    for i in range(N):
        try:
            data = json.load(open('data/%(i)d.json' % locals(), 'r'))
            if data and data.has_key('fields'):
                first_name = data['fields']['first_name'][0]['value'] if data['fields'].has_key('first_name') else ""
                last_name = data['fields']['last_name'][0]['value'] if data['fields'].has_key('last_name') else ""
                title = data['fields']['title'][0]['value'] if data['fields'].has_key('title') else ""
                q = "INSERT INTO person (first_name, last_name, title) VALUES (%s,%s,%s) RETURNING person_id"
                cur.execute(q, (first_name, last_name, title))
                person_id = cur.fetchone()[0]
                # entries in person_jobs
                if data and data.has_key('groups') and data['groups'].has_key('positions'):
                    for position in data['groups']['positions']:
                        company_id = None
                        role_id = None
                        # get the company id
                        if position.has_key('company'):
                            q = "SELECT company_id FROM company WHERE company_name=%s"
                            cur.execute(q, (position['company'][0]['value'], ))
                            company_id = cur.fetchone()[0]
                        # get the role id
                        if position.has_key('role'):
                            q = "SELECT role_id FROM role WHERE role_name=%s"
                            cur.execute(q, (position['role'][0]['value'], ))
                            role_id = cur.fetchone()[0]
                        # insert
                        q = "INSERT INTO person_jobs (person_id, company_id, role_id) VALUES (%s,%s,%s)"
                        cur.execute(q, (person_id, company_id, role_id))
                elif data and data.has_key('fields') and data['fields'].has_key('title'):
                    tparts = data['fields']['title'][0]['value'].split(' at ')
                    if len(tparts) > 1:
                        role = tparts[0].strip()
                        company = tparts[1].strip()
                        company_id = None
                        role_id = None
                        # get the company id
                        q = "SELECT company_id FROM company WHERE company_name=%s"
                        cur.execute(q, (company, ))
                        company_id = cur.fetchone()[0]
                        # get the role id
                        q = "SELECT role_id FROM role WHERE role_name=%s"
                        cur.execute(q, (role, ))
                        role_id = cur.fetchone()[0]
                        # insert
                        q = "INSERT INTO person_jobs (person_id, company_id, role_id) VALUES (%s,%s,%s)"
                        cur.execute(q, (person_id, company_id, role_id))
                # entries in person_skills
                if data and data.has_key('fields') and data['fields'].has_key('skills'):
                    for skill in data['fields']['skills']:
                        # get the skill id
                        q = "SELECT skill_id FROM skill WHERE skill_name=%s"
                        cur.execute(q, (skill['value'], ))
                        skill_id = cur.fetchone()[0]
                        # insert
                        q = "INSERT INTO person_skills (person_id, skill_id) VALUES (%s,%s)"
                        cur.execute(q, (person_id, skill_id))
            conn.commit()
        except:
            print >> sys.stderr, 'failed for %(i)d.json' % locals()
            traceback.print_exc()
        else:
            print >> sys.stderr, 'done with %(i)d.json' % locals()
    cur.close()
    conn.close()

if __name__ == "__main__":
    skills()
    companies_and_roles()
    person_skills_and_jobs()
    print "done :)"