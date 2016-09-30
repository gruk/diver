# diver
Wellington Diving Weather Analyser
# diver

# Guide #

Ensure you have a diver.db database set up
Regularly run the Updater.py file to populate the database
Once you have enough data, run the diver.py file to analyse the data from the database.

# Building Database #

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