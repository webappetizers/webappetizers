from flask import Flask, render_template
from bokehbikeapp.bokehplot import plot
from bokeh.embed import components
from pymongo import MongoClient
import os
from bson import json_util
import json
import irisapp.irisplot as ip
from bokeh.util.string import encode_utf8
from bokeh.resources import INLINE


client = MongoClient('mongodb://localhost:27017')
print("Created client")
db = client.streets_db
print("Connected to streets_db")
streets = db.streets

app = Flask(__name__)

# os.environ['TODO_DB_1_PORT_27017_TCP_ADDR']

@app.route('/')
def myplot():
	for row in db.streets.find({'elevations': {'$exists': 0}},{'_id': 0, 'coords': 1}).limit(10):
		# lat1, lon1, lat2, lon2 = row['lat1'], row['lon1'], row['lat2'], row['lon2']
		print(row)
	p = plot()
	script, div = components(p)
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()
	html = render_template("index.html",
		the_div=div,
		the_script=script,
		js_resources=js_resources,
        css_resources=css_resources)
	return encode_utf8(html)

@app.route('/iris')
def irisplot():
	data = ip.get_df()
	feature_names = ip.get_features(data)
	current_feature_name = ip.get_name()
	# Create the plot
	plot = ip.create_figure(data, current_feature_name, 10)
		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()
	html = render_template("iris.html",
		script=script, div=div,
		feature_names=feature_names,
		current_feature_name=current_feature_name,
		js_resources=js_resources,
        css_resources=css_resources)
	return encode_utf8(html)

@app.route('/add')
def addelevs(start=0):
	# 826516 records
	db.streets.find({})
	gmap_api.get_elevations

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)