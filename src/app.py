from flask import Flask, render_template
from bokehbikeapp.bokehplot import plot
from bokeh.embed import components
from pymongo import MongoClient
import os
from bson import json_util
import json


app = Flask(__name__)

def get_db():
	client = MongoClient('mongodb://localhost:27017')
	print("Created client")
	db = client.streets_db
	print("Created streets_db")
	db.test_streets.drop()
	with open('utils/test_coords.json') as f:
		data = json.load(f)
	for i, street in enumerate(data):
		db.test_streets.insert(street)
		print("Saved item to database: ", i)

		if i == 100:
			break
	
		
	# os.environ['TODO_DB_1_PORT_27017_TCP_ADDR']

@app.route('/')
def myplot():
	p = plot("Austin")
	script, div = components(p)
	return render_template("index.html",the_div=div, the_script=script)

@app.route('/add')
def addelevs(start=0):
	# 826516 records
	gmap_api

if __name__ == "__main__":
	db = get_db()
	# app.run(host='0.0.0.0', debug=True)