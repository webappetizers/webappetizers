from app import app, db
from flask import Flask, render_template
from bokehbikeapp.bokehplot import plot, gmap
from bokeh.embed import components
from pymongo import MongoClient
import os
from bson import json_util
import json
import irisapp.irisplot as ip
from bokeh.util.string import encode_utf8
from bokeh.resources import INLINE
import requests
from statistics import mean


@app.route('/test')
def test():
	p = gmap()
	script, div = components(p)
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()
	title = 'Elevation'
	html = render_template("index.html",
		the_div=div,
		the_script=script,
		js_resources=js_resources,
        css_resources=css_resources,
        title=title)
	return encode_utf8(html)

@app.route('/')
def myplot():
	coords = db.streets.find({'elevations.elev1': {'$exists': 1}, 'elevations.elev2': {'$exists': 1}},{'_id': 0})

	lat1 = [x['coords']['lat1'] for x in coords]
	lon1 = [x['coords']['lon1'] for x in coords]
	lat2 = [x['coords']['lat2'] for x in coords]
	lon2 = [x['coords']['lon2'] for x in coords]
	elev1 = [x['elevs']['elev1'] for x in coords]
	elev2 = [x['elevs']['elev2'] for x in coords]

	print([x for x in coords])
	print('lat1: ', lat1)
	print('lon1: ', lon1)

	centerlat = sum(lat1) / len(lat1)
	centerlon = sum(lon1) / len(lon1)

	lats = [(sum(x)/len(x),sum(y)/len(y)) for x,y in zip(lat1, lat2)]
	lons = [(sum(x)/len(x),sum(y)/len(y)) for x,y in zip(lon1, lon2)]
	elevs = [sum(x)/len(x) for x in zip(elev1, elev2)]

	p = plot(lats,lons,elevs,centerlat,centerlon)
	script, div = components(p)
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()
	title = 'Elevation'
	html = render_template("index.html",
		the_div=div,
		the_script=script,
		js_resources=js_resources,
        css_resources=css_resources,
        title=title)
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
	# return encode_utf8(html)
	return html

@app.route('/add/<quantity>')
def addelevs(quantity):
	# 826516 records
	
	def calc_elev(lat, lon):
		location = str(lat) + ',' + str(lon)
		search_url = 'https://maps.googleapis.com/maps/api/elevation/json?'
		search_payload = {"key": os.environ.get('GOOGLE_API_KEY'),
						 'locations':location}
		search_req = requests.get(search_url, params=search_payload)
		search_json = search_req.json()
		elevation = search_json['results'][0]['elevation']

		return elevation

	def save_elev1(id, elev):
		db.streets.update({'_id': id}, {'$set': {'elevations.elev1': elev}})
		return

	def save_elev2(id, elev):
		db.streets.update({'_id': id}, {'$set': {'elevations.elev2': elev}})
		return

	# Get all the previously calculated elevation segments
	def check_point_elev(lat, lon):
		coord1 = db.streets.find_one({'elevations': {'$exists': 1}, 'lat1': lat, 'lon1': lon},{'_id': 0, 'elev1': 1})
		coord2 = db.streets.find_one({'elevations': {'$exists': 1}, 'lat2': lat, 'lon2': lon},{'_id': 0, 'elev2': 1})
		print('Coord1 = ', coord1)
		print('Coord2 = ', coord2)

		if coord1:
			return coord1['elev1']
		elif coord2:
			return coord2['elev2']
		else:
			return

	# Get coordinate pairs that don't have an elevation
	quantity = int(quantity)
	coords = db.streets.find({'elevations': {'$exists': 0}, 'coords': {'$exists': 1}}, {'coords': 1}).limit(quantity)

	new_elevations = 0
	for segment in coords:
		print(segment)
		lat1 = segment['coords']['lat1']
		lon1 = segment['coords']['lon1']
		lat2 = segment['coords']['lat2']
		lon2 = segment['coords']['lon2']
		
		elev1 = check_point_elev(lat1, lon1)
		elev2 = check_point_elev(lat2, lon2)
		_id = segment['_id']

		if elev1:
			print('elev1= ',elev1)
			save_elev1(_id, elev1)
		else:
			elev1 = calc_elev(lat1, lon1)
			print('New elev= ',elev1)
			save_elev1(_id, elev1)
			new_elevations += 1

		if elev2:
			print('elev2= ',elev2)
			save_elev2(_id, elev2)
		else:
			elev2 = calc_elev(lat2, lon2)
			print('New elev= ',elev2)
			save_elev2(_id, elev2)
			new_elevations += 1

	return encode_utf8('<h2>Added ' + str(new_elevations) + ' elevations</h2>')