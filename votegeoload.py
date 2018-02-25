import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = "[insert api key]"

serviceurl = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

conn = sqlite3.connect('geovote.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("nycpollsites.txt")
count = 0

#avoid owing google $$
for line in fh:
    if count > 70:
        print('Retrieved 70 locations, restart in 24 hours to finish')
        break
    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))

    try:
        data = cur.fetchone()[0]
        print("Found in database ", address)
        continue
    except:
        pass

    parms = dict()
    parms["query"] = address
    parms["key"] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        js = json.loads(data)

    except:
        print(data)
        continue
    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('Failure to retrieve =====')
        print(data)
        break

    cur.execute('''INSERT INTO Locations (address, geodata)
        VALUES (?, ?)''', (memoryview(address.encode()), memoryview(data.encode()) ))
    conn.commit()

    if count % 10 == 0:
        time.sleep(2)
print("run geovotedump.py to read the data from the database")
