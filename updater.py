#!/usr/bin/env python

# import modules
import urllib, json, sqlite3, re

# define variables
wellington_url = "http://metservice.com/publicData/hourlyObsAndForecast_wellington"
lyallsurf_url = "http://www.metservice.com/publicData/surfingForecast?location=lyall"
makarasurf_url = "http://www.metservice.com/publicData/surfingForecast?location=makar"
conn = sqlite3.connect('diver.db')

# reads data from url and inserts into database - weather table
def update_data_wellington(url):
	uh = urllib.urlopen(url)
	data = uh.read()
	print 'Retrieved',len(data),'characters'

	try: js = json.loads(str(data))
	except: js = None

	if 'actualData' not in js:
	    print '==== Failure To Retrieve ===='

	# loop through data
	for c in js["actualData"]:
		datetime = str(format_datetime_wellington(c["date"], c["timeFrom"]))
		day = format_day(c["date"])
		rainFall = c["rainFall"]
		windDir = "'" +c["windDir"]+"'"
		windSpeed = c["windSpeed"]
		swell = 1.0
		actual = "'Yes'"
		notes = "'None'"
		image = "'None'"
		query = conn.execute("INSERT or REPLACE into weather\
			(datetime, day, windDir, windSpeed, rainFall, swell, actual, notes, image)\
			VALUES(%s, %s, %s, %r, %r, %r, %s, %s, %s) \
			;" % (str(datetime), str(day), str(windDir), float(windSpeed), float(rainFall), float(swell), str(actual), str(notes), str(image)))
	# loop through furture data
	for f in js["forecastData"]:
		datetime = str(format_datetime_wellington(f["date"], f["timeFrom"]))
		day = format_day(f["date"])
		rainFall = f["rainFall"]
		windDir = "'"+f["windDir"]+"'"
		windSpeed = f["windSpeed"]
		swell = 1.0
		actual = "'No'"
		notes = "'None'"
		image = "'None'"
		query = conn.execute("INSERT or REPLACE into weather\
			(datetime, day, windDir, windSpeed, rainFall, swell, actual, notes, image)\
			VALUES(%s, %s, %s, %r, %r, %r, %s, %s, %s)\
			;" % (str(datetime), str(day), str(windDir), float(windSpeed), float(rainFall), float(swell), str(actual),str(notes), str(image)))
	conn.commit()


# reads data from url and inserts into database
def update_data_surf(url, table):
	uh = urllib.urlopen(url)
	data = uh.read()
	print 'Retrieved',len(data),'characters'

	try: js = json.loads(str(data))
	except: js = None

	if 'forecast' not in js:
	    print '==== Failure To Retrieve ===='

	# loop through data
	for f in js["forecast"]:
		datetime = str(format_datetime_surf(f["date"]))
		# date = f["date"]
		# print "test swell dir " + f["swellDir"]
		# print "test swell height " + f["swellHeight"]
		swellHeight = f["swellHeight"]
		swellDir = "'"+f["swellDir"]+"'"
		windDir = "'"+f["windDir"]+"'"
		windSpeed = f["windSpeed"]
		# print date
		# print datetime, swellHeight, swellDir, windSpeed, windDir

		query = conn.execute("INSERT or REPLACE into %s\
			(datetime, windDir, windSpeed, swellDir, swellHeight)\
			VALUES(%s, %s, %s, %s, %s)\
			;" % (table, str(datetime), str(windDir), float(windSpeed), str(swellDir), float(swellHeight)))
	conn.commit()
	# query = conn.execute("SELECT * FROM lyall")
	# for row in query:
	# 	print row


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

update_data_wellington(wellington_url)
update_data_surf(makarasurf_url, 'makara')
update_data_surf(lyallsurf_url, 'lyall')
print "Job Done"
conn.close()


# DATABASE QUERIES:

# sqlite3 diver.db

# CREATE TABLE weather(
# datetime string PRIMARY KEY,
# day string,
# windDir string,
# windSpeed blob,
# rainFall blob,
# swell blob,
# actual string,
# notes string,
# image string
# );

# CREATE TABLE makara(
# datetime string PRIMARY KEY,
# windDir string,
# windSpeed blob,
# swellDir string,
# swellHeight blob
# );

# CREATE TABLE lyall(
# datetime string PRIMARY KEY,
# windDir string,
# windSpeed blob,
# swellDir string,
# swellHeight blob
# );

# CREATE TABLE tide(
# tideID integer PRIMARY KEY AUTOINCREMENT,
# datetime string,
# actualDatetime string,
# tide string
# );

# INSERT or REPLACE into weather(
# datetime, windDir, windSpeed, rainFall, swell)
# VALUES(
# 201512120830, 'N', 5.0, 0.0, 1.0);

# INSERT INTO weather(
# datetime, windDir, windSpeed, rainFall, swell)
# VALUES(
# 201512100000, 'N', 13, 0.0, 0);
