from bokeh.io import show, output_file, output_notebook
from bokeh.plotting import figure
from bokeh.io import show, output_file, output_notebook
from bokeh.models import(GMapPlot, GMapOptions, ColumnDataSource,
                        Circle, Line, Range1d, PanTool, WheelZoomTool, BoxSelectTool, )
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.palettes import Viridis3, Viridis256
from bokeh.models.glyphs import MultiLine

import pandas as pd
import math

import utils.get_data
from utils.YOUR_API_KEY import key


# def map_options():
# 	options = GMapOptions(lat=29.936, lng=-98.208,
#                          map_type='roadmap', zoom=14)
# 	return options

def plot():
	options = GMapOptions(lat=29.936, lng=-98.208,
                         map_type='roadmap', zoom=14)
	plot = figure(title='Austin Test')
	plot = GMapPlot(x_range=Range1d(),
	                y_range=Range1d(),
	                map_options=options,
	                api_key=key)
	# plot.title.text = title
	#plot.api_key=key
	plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

	# Call data() for the elevations. Will use this later for lat,lon
	datadict = utils.get_data.data()
	lon = datadict['lon']
	lat = datadict['lat']
	elev = datadict['elev']
	print('data[0] of lat: {}, lon: {}, elev: {}'.format(lat[0],lon[0],elev[0]))
	print('Count of lat: {}, lon: {}, elev: {}'.format(len(lat),len(lon),len(elev)))
	
	# Color Mapper
	low = math.floor(min(elev))
	high = math.ceil(max(elev))
	print('low_elev: {}, high_elev: {}'.format(low,high))

	mapper = LinearColorMapper(palette=Viridis256, low=low, high=high)
	color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
	plot.add_layout(color_bar, 'right')

	# MultiLine glyphs
	source = ColumnDataSource(
	    data=dict(
	        x=lon,
	        y=lat,
	        elev=elev,
	    )
	)
	print('Adding glyphs')
	line = MultiLine(xs="x",ys="y", line_color = {'field': 'elev', 'transform': mapper}, line_width=2.5)
	plot.add_glyph(source, line)
	print('Glyphs added')
	print(plot)
	return plot
