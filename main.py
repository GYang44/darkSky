import json
import datetime
import time
import requests

class darksky:
	lat = float(0)
	lon = float(0)
	key = None
	outputFile = None
	timeZoneOffSet = 0
	startTime = 0
	endTime = 0
	
	def __init__(self, start_time, end_time, timeZoneOffSet, lat, lon, key='bcf7d34f1cf44187f6f64c10990ab7eb'):
		self.key = key
		self.timeZoneOffSet = timeZoneOffSet
		self.lat = float(lat)
		self.lon = float(lon)
		self.startTime = self.convertTime(start_time)
		self.endTime = self.convertTime(end_time)

		return

	def convertTime(self, inTime):
		dt = datetime.datetime.strptime(inTime,'%Y-%m-%d')
		return int(time.mktime(dt.timetuple()))+ self.timeZoneOffSet * 3600

	def recoverTime(self, inTime):
		return datetime.datetime.fromtimestamp(int(inTime) - self.timeZoneOffSet * 3600).strftime('%Y-%m-%d %H:%M:%S')


	def getData(self, url):
		data = None
		try:
			r = requests.get(url)
			data = r.json()
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)
		return data

	def makeUrl(self, requestDay):
		url = 'https://api.darksky.net/forecast/{}/{},{},{}?hourly,unit=si'.format(self.key,self.lat,self.lon, requestDay)
		return url

	def createCSV(self, fileName):
		currentDay = self.startTime
		outputFile = open(fileName, 'w')
		while currentDay <= self.endTime:
			url = self.makeUrl(currentDay)
			#Remove this
			#url = 'https://www.guojunyang.net/TMP/test.json'
			print('Requesting: {}'.format(url))
			currentDay = currentDay + 3600*24
			data = self.getData(url)
			for hourData in data['hourly']['data']:
				"""
				time: 1325397600,
				summary: "Clear",
				icon: "clear-night",
				precipIntensity: 0,
				precipProbability: 0,
				temperature: 49.73,
				apparentTemperature: 47.48,
				dewPoint: 43.38,
				humidity: 0.79,
				pressure: 1019.06,
				windSpeed: 5.73,
				windBearing: 316,
				cloudCover: 0.05,
				visibility: 8.07
				"""
				outputFile.write(
					'{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(
						self.recoverTime(hourData['time']), 
						hourData['summary'], 
						hourData['icon'], 
						hourData['precipIntensity'], 
						hourData['precipProbability'],
						hourData['temperature'],
						hourData['apparentTemperature'],
						hourData['dewPoint'],
						hourData['humidity'],
						hourData['pressure'],
						hourData['windSpeed'],
						hourData['windBearing'],
						#hourData['cloudCover'],
						hourData['visibility'],
						)
					)
		outputFile.close()
		return

	#replace with your key

#year, month, day, timezone(offset to UTC in hours)
#print (convertTime('2012-1-1',1))
#print (convertTime('2012-1-1',-1))


dataFetcher = darksky('2016-1-1', '2016-2-2', -6, 29.4241, -98.4936)
dataFetcher.createCSV('./result.csv')
"""
requestUrl = makeUrl(key,location[0],location[1],convertTime('2012-1-1',6))
print('requesting: {}'.format(requestUrl))

data = getData('https://www.guojunyang.net/TMP/test.json')
print(recoverTime(data['hourly']['data'][-1]['time'], 6))
"""

#link = makeLink(key, location)
