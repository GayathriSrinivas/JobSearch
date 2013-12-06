from flask import Flask
import requests
import json
import urllib2
from flask import request,redirect,Response
#import MySQLdb
from flask import render_template
from collections import OrderedDict

from OpenSSL import SSL
import xlrd
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('/Users/snehakulkarni/Documents/CMPE273/myproject/Box_uploadDownload/certs2/server.key')
context.use_certificate_file('/Users/snehakulkarni/Documents/CMPE273/myproject/Box_uploadDownload/certs2/server.crt')

app = Flask(__name__)

year=0
noOfEmployees=0

"""
@app.route('/stats')
def getStatistics():
	url = 'http://api.bls.gov/publicAPI/v1/timeseries/data/'
	payload = {"seriesid":[ "CES0000000001" ] , "startyear":"2003", "endyear":"2013"} #, "CES0500000001" ] 
	headers = {'Content-Type': 'application/json'}

	response = requests.post(url, data=json.dumps(payload), headers=headers)
	#print response.json['Results']['series']
	jsondata = response.json['Results']['series']
	#number=0
	l=[]
	l.append(('year','Total Non-Farm'))
	for dataItem in jsondata:
		#lItem=[]
		dataFilter=dataItem['data']
		for dataElement in dataFilter:
			if (dataElement['periodName']=='May'):
				year=int(dataElement['year'])
				noOfEmployees=int(dataElement['value'])
				l.append((year,noOfEmployees))
	print "l-----" + str(l)			
	jsonString = json.dumps(l)
	print "mod---" + jsonString.replace("\"","'")
	return render_template('LineChart1.html',list=jsonString.replace("\"","'"))
	#return "hello"
		#(json.dumps(l,indent =4))
		#l.append(lItem)
		#print (json.dumps(l,indent =6))
	#numberofDataitems=response.iter_content
	#jsondata =    #r["Results"]["series"]["data"]
	#print json.dumps(jsondata)
@app.route('/series')
"""

#@app.route('/result',methods=['POST'])
def computeSeries():
	sectorID=request.form['sectorList']
	print sectorID
	return getSeriesStatistics()

@app.route('/test')
def testData():
	print 'In the testData'
	return render_template('OccupationDemo.html')

@app.route('/main')
def showSectorData():
	listofSeries=[]
	sectorDataList=[]
	#create a dictionary for each major sector with seriesid as key and sector name as value
	wb = xlrd.open_workbook('/Users/snehakulkarni/Documents/CMPE272/ProjectTeam32/Data/CESSupersectorCode.xlsx')
	sh = wb.sheet_by_index(0)

	for rownum in range(1, sh.nrows):
	    series = []
	    sid=''
	    code=''
	    row_values = sh.row_values(rownum)
	    code= str(row_values[0])
	    if row_values[0]<10:
	    	sid='CES0'+ code.split('.')[0]+'00000001'
	    else:
	    	sid='CES'+ code.split('.')[0] +'00000001'
	    series.append(sid)
	    series.append(row_values[1])
	    listofSeries.append(series)

	    #eachsectorData=getDatafromBLS(sid)
 
	# Serialize the list of dicts to JSON
	listofSectors = json.dumps(listofSeries)
	print '----------------------------------'
	print 'list of sectors'+listofSectors
	print '----------------------------------'
	
	#for eachsector in range(len(listofSectors)):
	#	url = 'http://api.bls.gov/publicAPI/v1/timeseries/data/'
		#print eachsector#[0]
		#payload = {"seriesid":

	return render_template('LineChart1.html',list='',data=listofSectors,value='')

@app.route('/result',methods=['POST'])
def getDatafromBLS():
	sectorID=request.form['sectorList']
	print sectorID
	url = 'http://api.bls.gov/publicAPI/v1/timeseries/data/'
	payload = {"seriesid":[ "CES4000000001" ] , "startyear":"2003", "endyear":"2013"} 
	headers = {'Content-Type': 'application/json'}

	response = requests.post(url, data=json.dumps(payload), headers=headers)
	#print response.json['Results']['series']
	jsondata = response.json['Results']['series']
	#number=0
	#print "jsondata-----" + json.dumps((jsondata),indent =4)	
	superl=[]
	l=[]
	for dataItem in jsondata:
		dataFilter=dataItem['data']
		#lItem=[] Data for one series obtained here
		#TODO: 
		l.append(('year','No noOfEmployees'))
		for dataElement in dataFilter:
			if (dataElement['periodName']=='May'):
				year=int(dataElement['year'])
				noOfEmployees=int(str(dataElement['value']).split('.')[0])
				l.append((year,noOfEmployees))
		#superl.append(l)

	print '==========================================='
	print json.dumps(l)
	print '==========================================='

	#print 'superl----' +json.dumps(superl)

	jsonString = json.dumps(l)
	print "mod---" + jsonString.replace("\"","'")
	return  render_template('LineChart1.html',list=jsonString.replace("\"","'"),data="",value='')
"""
@app.route('/stats')
def getSeriesStatistics():
	
	# Open the workbook
	wb = xlrd.open_workbook('/Users/snehakulkarni/Documents/CMPE272/ProjectTeam32/testBook.xlsx')

	# Print the sheet names
	print wb.sheet_names()

	# Get the first sheet either by index or by name
	sh = wb.sheet_by_index(0)

	listItems=[]
	# Iterate through rows, returning each as a list that you can index:
	for rownum in range(sh.nrows):
		listItems.append(sh.row_values(rownum))
	print json.dumps(listItems,indent=4)

	# If you just want the first column:
	first_column = json.dumps(sh.col_values(0))
	print first_column
	values = json.dumps(sh.col_values(1))
	print values

	url = 'http://api.bls.gov/publicAPI/v1/timeseries/data/'
	payload = {"seriesid":[ "CES0000000001" , "CES0500000001" ] , "startyear":"2003", "endyear":"2013"} 
	headers = {'Content-Type': 'application/json'}

	response = requests.post(url, data=json.dumps(payload), headers=headers)
	#print response.json['Results']['series']
	jsondata = response.json['Results']['series']
	#number=0
	#print "jsondata-----" + json.dumps((jsondata),indent =4)	
	superl=[]
	l=[]
	for dataItem in jsondata:
		dataFilter=dataItem['data']
		#lItem=[] Data for one series obtained here
		#TODO: 
		l.append(('year','Total Non-Farm'))
		for dataElement in dataFilter:
			if (dataElement['periodName']=='May'):
				year=int(dataElement['year'])
				noOfEmployees=int(dataElement['value'])
				l.append((year,noOfEmployees))
		superl.append(l)
	print json.dumps(superl)

	jsonString = json.dumps(l)
	print "mod---" + jsonString.replace("\"","'")
	return render_template('LineChart1.html',list=jsonString.replace("\"","'"),data="",value="")
	#return "hello"
		#(json.dumps(l,indent =4))
		#l.append(lItem)
		#print (json.dumps(l,indent =6))
	#numberofDataitems=response.iter_content
	#jsondata =    #r["Results"]["series"]["data"]
	#print json.dumps(jsondata)
"""
	# Open database connectiond
	db = MySQLdb.connect(host="localhost", 
						user="sneha", # your username
                      passwd="snehapass", # your password
                      db="DreamJobData") 
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Select qSQL with id=4.
	cursor.execute("SELECT qSQL FROM data WHERE year=1")

	# Fetch a single row using fetchone() method.
	results = cursor.fetchone()

	qSQL = results[0]

	cursor.execute(qSQL)

	# Fetch all the rows in a list of lists.
	qSQLresults = cursor.fetchall()
	for row in qSQLresults:
	    year = row[0]
	    noOfEmp = row[1]

	    #SQL query to INSERT a record into the table FACTRESTTBL.
	    cursor.execute('''INSERT into data (year, noOfEmp)
	                  values (%s, %s)''',
	                  (year, noOfEmployees))

	    # Commit your changes in the database
	    db.commit()

	# disconnect from server
	db.close()
"""
"""

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=5500,ssl_context=context)
	#getStatistics()
