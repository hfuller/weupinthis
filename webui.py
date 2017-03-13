from __future__ import print_function
import json
import sqlite3
from flask import Flask, redirect, request
import youtube_dl

app = Flask(__name__)

@app.route('/plays/latest.json')
def get_latest_json():
	print("Retrieving latest in db...")
	cur.execute('''SELECT * FROM plays ORDER BY played_at DESC LIMIT 1;''')
	latest = cur.fetchone()
	print(latest)

	#but we need a dict
	latest = row_to_dict(latest)
	print(latest)

	return json.dumps(latest)

@app.route('/plays')
def get_plays_json():
	skip = request.args['skip']
	print("Retrieving plays after", skip)
	cur.execute('''SELECT * FROM plays WHERE played_at > ? ORDER BY played_at ASC LIMIT 1;''', [skip])
	row = cur.fetchone()
	if row == None:
		return json.dumps(row)
	return json.dumps(row_to_dict(row))

@app.route('/plays/<played_at>/youtube')
def get_play_youtube(played_at):
	cur.execute('''SELECT * FROM plays WHERE played_at = ?;''', [played_at])
	row = cur.fetchone()
	print(row)
	try:
		return ydl.extract_info("gvsearch1:" + row["artist"] + " " + row["song"], False)["entries"][0]["id"]
	except:
		return ydl.extract_info("gvsearch1:" + row["song"], False)["entries"][0]["id"]

@app.route('/plays/random.json')
def get_random_json():
	cur.execute('''SELECT * FROM plays ORDER BY RANDOM() LIMIT 1;''')
	return json.dumps(row_to_dict(cur.fetchone()))


def row_to_dict(row):
	return {row.keys()[i]:row[i] for i in range(len(row))}


if __name__ == "__main__":
	print("Starting DB")
	db = sqlite3.connect('weupinthis.sqlite3')
	db.row_factory = sqlite3.Row

	print("init youtube-dl")
	ydl = youtube_dl.YoutubeDL({})

	db.execute('''CREATE TABLE IF NOT EXISTS plays(id INTEGER PRIMARY KEY AUTOINCREMENT, played_at TEXT, artist TEXT, song TEXT);''')
	cur = db.cursor()
	#app.debug = True #enables threading, so don't do it.
	app.run(host='0.0.0.0',port=6001)

