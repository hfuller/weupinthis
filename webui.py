from __future__ import print_function
import json
import sqlite3
from flask import Flask, redirect, request

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
	cur.execute('''SELECT * FROM plays WHERE played_at > ? ORDER BY played_at DESC LIMIT 1;''', [skip])
	return json.dumps(row_to_dict(cur.fetchone()))

@app.route('/plays/random')
def get_random_json():
	cur.execute('''SELECT * FROM plays ORDER BY RANDOM() LIMIT 1;''')
	return json.dumps(row_to_dict(cur.fetchone()))


def row_to_dict(row):
	return {row.keys()[i]:row[i] for i in range(len(row))}


if __name__ == "__main__":
	print("Starting DB")
	db = sqlite3.connect('weupinthis.sqlite3')
	db.row_factory = sqlite3.Row

	db.execute('''CREATE TABLE IF NOT EXISTS plays(id INTEGER PRIMARY KEY AUTOINCREMENT, played_at TEXT, artist TEXT, song TEXT);''')
	cur = db.cursor()
	#app.debug = True #enables threading, so don't do it.
	app.run(host='0.0.0.0',port=6001)

