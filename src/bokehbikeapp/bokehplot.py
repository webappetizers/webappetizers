from bokeh.io import show, output_file, output_notebook
from bokeh.plotting import figure
from bokeh.io import show, output_file, output_notebook
from bokeh.models import(GMapPlot, GMapOptions, ColumnDataSource,
                        Circle, Line, Range1d, PanTool, WheelZoomTool,
                        BoxSelectTool, ColorBar, LinearColorMapper)
from bokeh.palettes import Viridis3, Viridis256
from bokeh.models.glyphs import MultiLine

import pandas as pd
import math

import utils.get_data
from utils.YOUR_API_KEY import key
import os

def gmap(lat=30.29, lng=-97.73):
	options = GMapOptions(lat=lat, lng=lng, map_type='roadmap', zoom=12)
	api_key = os.environ.get('GOOGLE_API_KEY')
	plot = GMapPlot(x_range=Range1d(),
	                y_range=Range1d(),
	                map_options=options,
	                api_key = api_key)
	
	mapper = LinearColorMapper(palette=Viridis256, low=0, high=100)
	color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
	plot.add_layout(color_bar, 'right')

	# MultiLine glyphs
	source = ColumnDataSource(
    data=dict(
        lat=[(30.29, 30.20)], #, 30.29],
        lon=[(-97.70, -97.74)], #-97.78],
        elev=[50]
    	)
	)

	# plot = figure()
	circle = Circle(x="lon", y="lat", size=15, line_color = {'field': 'elev', 'transform': mapper}, line_width=2.5) # fill_color="blue", fill_alpha=0.8, line_color=None)
	# plot.add_glyph(source, circle)
	line = MultiLine(xs="lon",ys="lat", line_color = {'field': 'elev', 'transform': mapper}, line_width=5.5)
	print(line)
	plot.add_glyph(source, line)
	plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
	return plot

def plot(lats,lons,elevs,centerlat,centerlon):

	# Color Mapper
	low = math.floor(min(elevs))
	high = math.ceil(max(elevs))
	print('low_elev: {}, high_elev: {}'.format(low,high))

	# Initialize plot
	plot = gmap(centerlon,	centerlat)
	plot.title.text = 'Austin'
	# plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

	mapper = LinearColorMapper(palette=Viridis256, low=low, high=high)
	color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
	plot.add_layout(color_bar, 'right')

	# MultiLine glyphs
	source = ColumnDataSource(
	    data=dict(
	        x=lons,
	        y=lats,
	        elev=elevs,
	    )
	)

	# source = ColumnDataSource(
 #    data=dict(
 #        x=[30.29, 30.20, 30.29],
 #        y=[-97.70, -97.74, -97.78],
 #        elev=[1,50,100],
 #    	)
	# )
	print('Adding glyphs')
	line = MultiLine(xs="x",ys="y", line_color = {'field': 'elev', 'transform': mapper}, line_width=2.5)
	plot.add_glyph(source, line)
	print('Glyphs added')
	print(plot)
	return plot
