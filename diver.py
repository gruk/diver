#!/usr/bin/env python

# import modules
import sqlite3, re
from time import localtime, strftime

# define variables
conn = sqlite3.connect('diver.db')

# main
def main():
	# databasedump()
	# print get_time()
	selector()

def selector():
	print ''
	print 'Welcome to the Diving weather machine'
	print 'Hit 1 for the South Coast report'
	option = raw_input("or 'n' to quit: ")
	if option == '1':
		print ''
		lyall_bay(get_time())
	elif option == '':
		exit()
	elif option == 'n':
		exit()
	else:
		selector()



def get_time():
	current_time = strftime("%Y%m%d%H%M", localtime())
	# current_time = '201512152359' # for testing
	if int(current_time[8:10]) % 2 != 0:
		new_10 = int(current_time[8:10]) - 1
		if new_10 < 10:
			new_10 = '0' + str(new_10)
		rounded_time = current_time[0:8] + str(new_10) + '00'
	else:
		rounded_time = current_time[0:10] + '00'
	return rounded_time


# read from database and print to console
# for troubleshooting purposes
def databasedump():
	query = conn.execute(" SELECT * \
		FROM weather;")
	for row in query:
		print row
	conn.close()

def south_coast():
	query = conn.execute(" SELECT windDir \
		FROM weather;")
	for row in query:
		pass

def lyall_bay(time):
	# Declaring local variables
	wind_problems = []
	swell_problems = []
	wind_forcast_good = []
	wind_forcast_bad = []
	swell_forcast_good = []
	swell_forcast_bad = []
	swellHeight = -20
	rainfall = 0
	# Reading database
	query = conn.execute("SELECT weather.datetime, weather.windDir, weather.windSpeed, lyall.windDir, lyall.windSpeed, lyall.swellHeight, lyall.swellDir, weather.rainFall\
		FROM weather\
		LEFT JOIN lyall on lyall.datetime = weather.datetime\
		ORDER BY weather.datetime DESC\
		LIMIT 48;")
		
	# Parsing through data	
	for row in query:
		# sets swellHeight to whatever the current row says it is
		if row[5] is None:
			pass
		else:
			swellHeight = row[5]

		# collecting wind data from past
		if int(time) > int(row[0]):
			if str(row[3]) is None:
				if str(row[1]) == 'S' or str(row[1]) == 'SE' or str(row[1]) == 'SW':
					wind_problems.append(row)
			elif str(row[3]) == 'S' or str(row[3]) == 'SE' or str(row[3]) == 'SW':
					wind_problems.append(row)

		# collecting swell data from past
		if int(time) > int(row[0]):
			if row[5] is None:
				pass
			elif row[5] > 2.0:
					swell_problems.append(row)		
		
		# collecting rainfall data from past:
		if int(time) > int(row[0]):
			rainfall += row[7]

		# when loop hits current time 
		# this is where current conditions are set
		# if current time isn't in the dataset this won't run
		if int(time) == int(row[0]):
			print 'Current conditions at lyall bay:'
			print 'at %s' % format_date(str(time))
			# collecting wind speed and direction first from lyall table, and secondarily from wellington data
			if row[3] is None:
				windDir = row[1]
			else:
				windDir = row[3]
			if row[4] is None:
				windSpeed = row[2]
			else:
				windSpeed = row[4]

			# Current Conditions
			print 'Wind Direction: %s' % (windDir)
			current_wind_direction = windDir
			print 'Wind Speed: %r km/h' % (windSpeed)
			current_wind_speed = windSpeed
			if swellHeight == -20:
				print 'Swell Height unknown'
				# set the current time's swell to whatever the most recent valid swell was and saves it in a new variable
				current_swell_height = swellHeight
			else:
				print 'Swell Height: %rm' % (swellHeight)
				# set the current time's swell to whatever the most recent valid swell was and saves it in a new variable
				current_swell_height = swellHeight
			print ''
		
		# collecting forcast wind data
		if int(time) < int(row[0]):
			if str(row[3]) is None:
				if str(row[1]) == 'S' or str(row[1]) == 'SE' or str(row[1]) == 'SW':
					wind_forcast_bad.append(row)
				elif str(row[1]) == 'N' or str(row[1]) == 'NE' or str(row[1]) == 'NW':
					wind_forcast_good.append(row)
			elif str(row[3]) == 'N' or str(row[3]) == 'NE' or str(row[3]) == 'NW':
					wind_forcast_good.append(row)
			elif str(row[3]) == 'S' or str(row[3]) == 'SE' or str(row[3]) == 'SW':
					wind_forcast_bad.append(row)

		# elif row[0] > time:
			# 	print 'FORECAST'
			# 	print '%s wind forcast at %s' % (format_direction(str(row[1])), format_date(str(row[0])))
			# 	print 'Weather might turn on you'
			# 	print ''

	# passing data to the analysis functions
	analyse_swell(current_swell_height, swell_problems)
	analyse_wind(current_wind_direction, wind_problems, time)
	analyse_rainfall(rainfall)


def analyse_swell(current_swell, swell_problems):
	# analysing swell data
	if current_swell > 2.0:
		print 'Swell above 2m - Too rough right now'
	
	if len(swell_problems) == 0:
		pass
	else:
		print 'Poor Conditions for the south coast due to:'
		for prob in swell_problems:
			print 'EARLIER'
			print '%s swell of %sm detected at %s' % (format_direction(str(prob[6])), str(prob[5]), format_date(str(prob[0])))
			print ''


def analyse_wind(current_wind, wind_problems, time):

	if current_wind == 'S' or current_wind == 'SW' or current_wind == 'SE':
		print 'Southerly currently blowing, look at Makara'


	if len(wind_problems) == 0:
		print "Conditions are currently great for South Coast on %r" % format_date(time)
		print ''

	elif len(wind_problems) == 1:
		print 'Only one occurance of unfavorable wind over the last couple of days, things are probably ok'
		print 'This occurance is as follows:'
		for row in wind_problems:
			if row[0] < time:
				if row[3] is None:
					print 'EARLIER'
					print '%s winds detected at %s (NOT LOCAL TO LYALL BAY)' % (format_direction(str(row[1])), format_date(str(row[0])))
					print 'wind speed of %s km/h' % (str(row[2]))
					print 'Visibility likely ok'
					print ''
				else:
					print 'EARLIER'
					print '%s winds detected at %s (LOCAL TO LYALL BAY)' % (format_direction(str(row[3])), format_date(str(row[0])))
					print 'wind speed of %s km/h' % (str(row[4]))
					print 'Visibility probably ok'
					print ''
	else:
		print "Poor conditions for the south coast due to:"
		for row in wind_problems:
			if row[0] == time:
				print 'CURRENT'
				print '%s is blowing, Consider Makara' % (format_direction(str(row[1])))
				print ''
			elif row[0] < time:
				if row[3] is None:
					print 'EARLIER'
					print '%s winds detected at %s (NOT LOCAL TO LYALL BAY)' % (format_direction(str(row[1])), format_date(str(row[0])))
					print 'wind speed of %s km/h' % (str(row[4]))
					print ''
				else:
					print 'EARLIER'
					print '%s winds detected at %s (LOCAL TO LYALL BAY)' % (format_direction(str(row[3])), format_date(str(row[0])))
					print 'wind speed of %s km/h' % (str(row[4]))
					print ''
		print 'South Coast Visibility likely comprimised'
		print ''

def analyse_rainfall(rainfall):
	if rainfall > 10.0:
		print 'Rainfall from last two days is over 10mm, expect low Visibility'

def format_date(datetime):
	year = re.findall('^[0-9]{4}', datetime)[0]
	month = re.findall('^.{4}(.{2})',datetime)[0]
	day = re.findall('^.{6}(.{2})', datetime)[0]
	hour = re.findall('^.{8}(.{2})', datetime)[0]
	minute = re.findall('^.{10}(.{2})', datetime)[0]
	# datetime = year+month+day+hour+minute
	date = '%s/%s/%s' % (year, month, day)
	time = '%s:%s' % (hour, minute)
	return date + ' ' + time


def test():
	query = conn.execute("SELECT datetime FROM weather ORDER BY datetime DESC LIMIT 24;")
	for row in query:
		print 201512181200 - int(row[0])

def format_direction(direction):
	if direction == 'S':
		return 'Southerly'
	elif direction == 'SE':
		return "Sou'Easterly"
	elif direction == 'SW':
		return "Sou'Westerly"
	elif direction == 'N':
		return "Northerly"
	elif direction == 'NW':
		return "Nor'Westerly"
	elif direction == 'NE':
		return "Nor'Easterly"
	elif direction == 'W':
		return "Westerly"
	elif direction == 'E':
		return "Easterly"
	else:
		return direction


if __name__ == '__main__':
	main()
else:
	print 'You are not running this as main'
	main()



# TO DO:
# select correct data from database - last 3 days?
# Start working wind and rain forecasts in for future weather warnings

# DB queries:

# SELECT weather.datetime AS 'date', weather.rainFall AS 'Rain', lyall.swellHeight AS 'Swell', lyall.windDir AS 'Wind Dir', lyall.windSpeed AS 'Wind Speed'
# FROM weather
# LEFT JOIN lyall ON weather.datetime = lyall.datetime;

# SELECT lyall.datetime, lyall.windDir, lyall.windSpeed, lyall.swellHeight, lyall.swellDir, weather.rainFall
# FROM lyall
# LEFT JOIN weather on lyall.datetime = weather.datetime;

# SELECT weather.datetime, weather.windDir, weather.windSpeed, lyall.windDir, lyall.windSpeed, lyall.swellHeight, lyall.swellDir, weather.rainFall
# FROM weather
# LEFT JOIN lyall on lyall.datetime = weather.datetime
# ORDER BY weather.datetime DESC
# LIMIT 48;