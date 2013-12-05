#! /usr/bin/python

from flask import *
import json
import psycopg2
import urllib2

app = Flask(__name__)
fp = open('dbDetails.txt','r')
db_string = fp.read().strip()
fp.close()

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/skill_autocomplete')
def skill_autocomplete():
    term = request.args.get('term', '')
    if len(term) < 3:
        return json.dumps({})
    return json.dumps(get_skills(term))

@app.route('/skill_companies')
def skill_companies():
    skill = urllib2.unquote(request.args.get('skill', ''))
    return json.dumps(get_skill_companies(skill))

@app.route('/companies')
def companies():
    return render_template('companies.html')

@app.route('/g_companies')
def g_companies():
    return render_template('g_companies.html')

@app.route('/companies_autocomplete')
def companies_autocomplete():
    term = request.args.get('term', '')
    if len(term) < 3:
        return json.dumps({})
    return json.dumps(get_companies(term, "company"))

@app.route('/g_companies_autocomplete')
def g_companies_autocomplete():
    term = request.args.get('term', '')
    if len(term) < 3:
        return json.dumps({})
    return json.dumps(get_companies(term, "g_company"))

@app.route('/company_skills')
def company_skills():
    company = urllib2.unquote(request.args.get('company', ''))
    return json.dumps(get_company_skills(company))

@app.route('/company_salary')
def company_salary():
    company = urllib2.unquote(request.args.get('company', ''))
    salary = get_company_salary(company)
    info = render_template('company_info.html',info=get_company_info(company))
    return json.dumps({'salary' : salary , 'company_info' : info})

def get_skills(prefix):
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    try:
        skills = []
        q = "SELECT skill_id, skill_name FROM skill WHERE skill_name IS NOT NULL AND skill_name ILIKE %s LIMIT 5"
        cur.execute(q, ("%s%%" % prefix,))
        for row in cur:
            skills.append({'id': row[0], 'label': row[1], 'value': row[1]})
        return skills
    finally:
        cur.close()
        conn.close()

def get_skill_companies(skill):
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    try:
        companies = []
        q = """
            select
                company_name,
                count(1) * 100
            from
                person_skills ps
                join person_jobs using (person_id)
                join skill using (skill_id)
                join company using (company_id)
            where
                skill_name ilike %s
            group by
                company_name
            order by
                2 desc
            limit 
            5;
            """
        cur.execute(q, ("%s%%" % skill,))
        for row in cur:
            companies.append([row[0], row[1]])
        return companies
    finally:
        cur.close()
        conn.close()

def get_companies(prefix, table_name):
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    try:
        companies = []
        q = "SELECT company_id, company_name FROM %(table_name)s " % locals()
        condition = "WHERE company_name IS NOT NULL AND company_name ILIKE %s LIMIT 5"
        cur.execute(q+condition, ("%s%%" % prefix,))
        for row in cur:
            companies.append({'id': row[0], 'label': row[1], 'value': row[1]})
        return companies
    finally:
        cur.close()
        conn.close()

def get_company_skills(company):
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    try:
        skills = []
        q = """
            select
                skill_name,
                count(1) * 100
            from
                company
                join person_jobs using (company_id)
                join person_skills using (person_id)
                join skill using (skill_id)
            where
                company_name ilike %s
            group by
                skill_name
            order by
                2 desc
            limit
                5
            """
        cur.execute(q, ("%s%%" % company,))
        for row in cur:
            skills.append([row[0], row[1]])
        return skills
    finally:
        cur.close()
        conn.close()

def get_company_salary(company):
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    try:
        salary = []
        q = """
            select
                role_name,
                range_low,
                case 
                    when mean < range_low then ((range_low + range_high) / 2)::int
                    else mean
                end,
                range_high
            from
                g_salary
                join g_company using (company_id)
                join g_role using (role_id)
            where
                lower(company_name)=lower(%s)
            """
        cur.execute(q, (company,))
        for row in cur:
            salary.append([row[0], row[1], row[2], row[3]])
        return salary
    finally:
        cur.close()
        conn.close()

def get_company_info(company):
    conn = psycopg2.connect(db_string)
    cur = conn.cursor()
    try:
        salary = []
        q = """
            select
                company_id,
                website,
                type,
                revenue,
                location,
                ceo,
                industry,
                ceo_picture
            from
                g_company
            where
                lower(company_name) = lower(%s)
            """
        cur.execute(q, (company,))
        row = cur.fetchone()
        info = {}
        info['company_id'] = row[0]
        info['website'] = row[1] if 'http' in row[1] else "http://%s" % row[1]
        if "public" in row[2].lower():
            info['type'] = "Public"
        elif "private" in row[2].lower():
            info['type'] = "Private"
        else:
            info['type'] = "Unknown"
        info['revenue'] = row[3]
        info['location'] = row[4]
        info['ceo'] = row[5]
        info['industry'] = row[6]
        info['ceo_picture'] = row[7]
        print row[7]
        info['company_name'] = company
        info['competitors'] = []
        q = """
            select
                company_name
            from
                g_related_company
                join g_company on (g_company.company_id = g_related_company.company_id2)
            where
                company_id1 = %s
            """
        cur.execute(q, (info['company_id'],))
        for row in cur:
            if row[0] not in info['competitors']:
                info['competitors'].append(row[0])
        return info
    finally:
        cur.close()
        conn.close()



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)