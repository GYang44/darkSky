import json
import datetime
import time
import requests

def convertTime(inTime,timezoneOffSet):
	dt = datetime.datetime.strptime(inTime,'%Y-%m-%d')
	return int(time.mktime(dt.timetuple()))+ timezoneOffSet * 3600



def getData(url):
	data = None
	try:
		r = requests.get(url)
		data = r.json()
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(1)
	return data

def makeUrl(key,lat,lon,date):
	url = 'https://api.darksky.net/forecast/{}/{},{},{}?hourly,unit=si'.format(key,lat,lon,date)
	return url

#replace with your key
key = 'bcf7d34f1cf44187f6f64c10990ab7eb'

#
location = ['29.4241','-98.4936'] 

#year, month, day, timezone(offset to UTC in hours)
#print (convertTime('2012-1-1',1))
#print (convertTime('2012-1-1',-1))

requestUrl = makeUrl(key,location[0],location[1],convertTime('2012-1-1',6))
print('requesting: {}'.format(requestUrl))

print(getData(requestUrl))

#link = makeLink(key, location)
