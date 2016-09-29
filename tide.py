#!/usr/bin/env python

# import modules
import urllib, json, sqlite3, re

swell_url = "http://www.metservice.com/publicData/inshoreForecastWellington_Wellington_Karehana-Bay"
conn = sqlite3.connect('diver.db')

# reads data from url and inserts into database - weather table
def update_tide(url):
	uh = urllib.urlopen(url)
	data = uh.read()
	print 'Retrieved',len(data),'characters'
	# print data
 	try: js = json.loads(str(data))
 	except: js = None

 	if 'tides' not in js:
	    print '==== Failure To Retrieve ===='

	# loop through data
	for c in js["tides"]:
		if c["location"] == 'WELLINGTON':
			tide_height = c["tides"][0]["height"]
			high_tide_time = c["tides"][0]["time"]
			low_tide_time = low_tide_calc(format_datetime_tide(high_tide_time))
			query = conn.execute("INSERT or REPLACE into tide\
				(datetime, actualDatetime, tide)\
				VALUES(?, ?, ?)\
				;" (format_datetime_tide(high_tide_time,1),format_datetime_tide(high_tide_time,0),'high'))
# CREATE TABLE tide(
# tideID integer PRIMARY KEY AUTOINCREMENT,
# datetime string,
# actualDatetime string,
# tide string
# );
				
			tide_height = c["tides"][1]["height"]
			hight_tide_time = c["tides"][1]["time"]
	# 	datetime = str(format_datetime_wellington(c["date"], c["timeFrom"]))
	# 	day = format_day(c["date"])
	# 	rainFall = c["rainFall"]
	# 	windDir = "'" +c["windDir"]+"'"
	# 	windSpeed = c["windSpeed"]
	# 	swell = 1.0
	# 	actual = "'Yes'"
	# 	notes = "'None'"
	# 	image = "'None'"
	# 	query = conn.execute("INSERT or REPLACE into weather\
	# 		(datetime, day, windDir, windSpeed, rainFall, swell, actual, notes, image)\
	# 		VALUES(%s, %s, %s, %r, %r, %r, %s, %s, %s) \
	# 		;" % (str(datetime), str(day), str(windDir), float(windSpeed), float(rainFall), float(swell), str(actual), str(notes), str(image)))
	# # loop through furture data
	# for f in js["forecastData"]:
	# 	datetime = str(format_datetime_wellington(f["date"], f["timeFrom"]))
	# 	day = format_day(f["date"])
	# 	rainFall = f["rainFall"]
	# 	windDir = "'"+f["windDir"]+"'"
	# 	windSpeed = f["windSpeed"]
	# 	swell = 1.0
	# 	actual = "'No'"
	# 	notes = "'None'"
	# 	image = "'None'"
	# 	query = conn.execute("INSERT or REPLACE into weather\
	# 		(datetime, day, windDir, windSpeed, rainFall, swell, actual, notes, image)\
	# 		VALUES(%s, %s, %s, %r, %r, %r, %s, %s, %s)\
	# 		;" % (str(datetime), str(day), str(windDir), float(windSpeed), float(rainFall), float(swell), str(actual),str(notes), str(image)))
	# conn.commit()

# # reads data from url and inserts into database
# def update_data_surf(url, table):
# 	uh = urllib.urlopen(url)
# 	data = uh.read()
# 	print 'Retrieved',len(data),'characters'

# 	try: js = json.loads(str(data))
# 	except: js = None

# 	if 'forecast' not in js:
# 	    print '==== Failure To Retrieve ===='

# 	# loop through data
# 	for f in js["forecast"]:
# 		datetime = str(format_datetime_surf(f["date"]))
# 		# date = f["date"]
# 		swellHeight = f["swellHeight"]
# 		swellDir = "'"+f["swellDir"]+"'"
# 		windDir = "'"+f["windDir"]+"'"
# 		windSpeed = f["windSpeed"]
# 		# print date
# 		# print datetime, swellHeight, swellDir, windSpeed, windDir

# 		query = conn.execute("INSERT or REPLACE into %s\
# 			(datetime, windDir, windSpeed, swellDir, swellHeight)\
# 			VALUES(%s, %s, %s, %s, %s)\
# 			;" % (table, str(datetime), str(windDir), float(windSpeed), str(swellDir), float(swellHeight)))
# 	conn.commit()
# 	# query = conn.execute("SELECT * FROM lyall")
# 	# for row in query:
# 	# 	print row

def low_tide_calc(tide):
	# 201601012355
	int(tide) + 630
	if int(tide[10]) >= '6':
		int(tide[9]) += 1
		tide[10] = int(tide[10]) - 6
	if int(tide[8:10]) == 24:
		int(tide[8:10]) = 00
		int(tide[7]) += 1
	elif int(tide[8:10]) == 25:
		int(tide[8:10]) = 01
		int(tide[7]) += 1

# process the date and time into a single value in the format 201501010830
def format_datetime_wellington(date, time):
	year = re.findall('[0-9]+$', date)[0]
	month = convert_month(re.findall('\s([a-zA-Z]+)',date)[0])
	day = re.findall('([0-9]+)\s', date)[0]
	hour = re.findall('^[0-9]+', time)[0]
	minute = re.findall('[0-9]+$', time)[0]
	datetime = year+month+day+hour+minute
	return datetime

# collects the day from the date in three letter format
def format_day(date):
	day = "'" + re.findall('^[a-zA-Z]+',date)[0] + "'"
	return day

# process the date and time into a single value in the format 201501010830
def format_datetime_surf(date):
	year = re.findall('[0-9]+$', date)[0]
	month = convert_month(re.findall('([a-zA-Z]+)',date)[0])
	day = re.findall('\s([0-9]+)\s', date)[0]
	hour = re.findall('^[0-9]+', date)[0]
	minute = re.findall(':([0-9]+)', date)[0]
	if int(hour) <10:
		hour = '0'+ hour
	datetime = year+month+day+hour+minute
	return datetime

def format_datetime_tide(date, rounder):
	""" 
		takes two arguements, one being a date string in the format: 2:53am Saturday 16 Jan 2016
		the other being a 1 or 0. 1 will cause this function to return a rounded datetime
	"""
	
	year = re.findall('[0-9]+$', date)[0]
	month = convert_month(re.findall('[0-9]\s([a-zA-Z]{3})',date)[0])
	day = re.findall('\s([0-9]+)\s', date)[0]
	hour = str(re.findall('^([0-9]{2})' , date)[0])
	minute = str(re.findall(':([0-9]{2})' , date)[0])
	datetime = year+month+day+hour+minute
	if rounder == 1:
		if int(datetime[8:10]) % 2 != 0:
			new_10 = int(datetime[8:10]) - 1
			if new_10 < 10:
				new_10 = '0' + str(new_10)
			rounded_time = datetime[0:8] + str(new_10) + '00'
		else:
			rounded_time = datetime[0:10] + '00'
		return rounded_time
	elif rounder == 0:
		return datetime
	else:
		return datetime
		

	

# month conversion helper
def convert_month(month):
	if month == 'Jan':
		return '01'
	elif month == 'Feb':
		return '02'
	elif month == 'Mar':
		return '03'
	elif month == 'Apr':
		return '04'
	elif month == 'May':
		return '05'
	elif month == 'Jun':
		return '06'
	elif month == 'Jul':
		return '07'
	elif month == 'Aug':
		return '08'
	elif month == 'Sep':
		return '09'
	elif month == 'Oct':
		return '10'
	elif month == 'Nov':
		return '11'
	elif month == 'Dec':
		return '12'
	else:
		print 'Date Error'
		conn.close()
		exit()

update_tide(swell_url)
print "Job Done"
conn.close()