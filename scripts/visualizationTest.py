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



@app.route('/testVisual')
def showSalary():
	
	wb = xlrd.open_workbook('/Users/snehakulkarni/Documents/CMPE272/ProjectTeam32/sampleData.xlsx')
	sh = wb.sheet_by_index(0) # this is a sheet object
	#print json.dumps(sh)
	print sh.nrows
	print sh.ncols
	
	# List to hold dictionaries
	cars_list = []
	 
	# Iterate through each row in worksheet and fetch values into dict
	for rownum in range(0, sh.nrows):
	    #cars = OrderedDict()
	    row_values = sh.row_values(rownum)
	    rowedit=[]
	    state= 'US-'+ row_values[0]
	    noofEmployees = row_values[1]
	    wage = row_values[2]
	    rowedit.append(state)
	    rowedit.append(noofEmployees)
	    rowedit.append(wage)
	    cars_list.append(rowedit)
	print cars_list


	jsonString = json.dumps(cars_list)
	print jsonString.replace("\"","'")

	return render_template('exampleGeo.html', list=jsonString.replace("\"","'"))


if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=5600,ssl_context=context)
	#getStatistics()
