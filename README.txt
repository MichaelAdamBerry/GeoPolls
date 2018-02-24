# GeoPolls -A final project for Using Databases with Python. Developed by University of Michigan for Coursera. 
http://www.py4e.com

Description:
-geoload.py reads polling addresses from a text document and uses Google Maps API to retrieve the geolocation data. 
 geovote.sqlite database is created which stores text adress, latitude, and longitude data.

-geodump.py aquires data from geovote.sql and writes the latitude, longitude, and formatted address to where.js 

-where.html displays those locations on a map in browser.


Usage: 
Run geoload.py
Run geodump.py
Open where.html

Notes: 
geoload.py will only make 70 requests to Google in order to avoid usage limits. 
It instructs the user to reload in 24 hours to continue.
When all locations have been loaded into the database it will instruct user to run geodump.py


Requirements: 
Python 3.6
sqllite
Google Maps API Key - https://developers.google.com/maps/
