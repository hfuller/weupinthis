from __future__ import print_function
import requests
import json
import sqlite3

print("Starting DB")
db = sqlite3.connect('weupinthis.sqlite3')
db.execute('''CREATE TABLE IF NOT EXISTS plays(id INTEGER PRIMARY KEY AUTOINCREMENT, played_at TEXT, artist TEXT, song TEXT);''')
cur = db.cursor()

print("Retrieving latest in db...")
cur.execute('''SELECT played_at FROM plays ORDER BY played_at DESC LIMIT 1;''')
latest = cur.fetchone()
if latest == None:
	latest = ""
else:
	latest =  latest[0]

url = "http://api.tunegenie.com/v1/brand/nowplaying/?apiid=entercom&b=weup&since=" + latest
print("grabbing plays since", latest, "-", url)
plays = requests.get(url)
plays = json.loads(plays.text)["response"]
#We reverse the list because it is returned with the newest play first.
#It isn't strictly necessary but it should help keep the date incrementing with the id.
plays.reverse()
for play in plays:
	print(play['played_at'] + ": " + play['artist'] + " - " + play['song'])
	cur.execute('''SELECT id FROM plays WHERE played_at = '%s';''' % play['played_at'])
	if cur.fetchone() == None:
		cur.execute('''INSERT INTO plays(played_at, artist, song) VALUES(?, ?, ?);''', [ play['played_at'], play['artist'], play['song'] ])
	else:
		print("Skipped because already present in db.")
db.commit()
print("Committed the db.")

