from glassdoor import get
import json
import traceback


def glassdoor_get_company_details():
 count = 0
 fp = open('company_list.txt','r')
 for line in fp:
  try:
   x = get(line)
   x = x.json()
   result = json.loads(x)
  except: 
   continue
  try:
   if result.get('satisfaction',None):
    count +=1
    title = "company1/"+str(count)+'.json'
    f = open(title,'w')
    f.write(json.dumps(result))
    f.close()
  except:
   print ':('
   print traceback.format_exc()

if __name__ == '__main__':
 glassdoor_get_company_details()
