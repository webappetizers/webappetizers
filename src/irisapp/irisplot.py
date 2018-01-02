from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure


def get_df():
	iris_df = pd.read_csv("src/data/iris.data", names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
	return iris_df

def get_features(iris_df):
	feature_names = iris_df.columns[0:-1].values.tolist()
	return feature_names

def get_name():
	current_feature_name = request.args.get("feature_name")
	if current_feature_name == None:
		current_feature_name = "Sepal Length"
	return current_feature_name

# Create the main plot
def create_figure(data, current_feature_name, bins):
		
	# p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species', 
	#  	bins=bins, legend='top_right', width=600, height=400)
	
	print(data[current_feature_name].head())
	hist, edges = np.histogram(data[current_feature_name], density=True, bins=bins)
	print(hist)
	print(edges)
	p = figure()
	p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:]) #, line_color="Species")

	# Set the x axis label
	p.xaxis.axis_label = current_feature_name

	# Set the y axis label
	p.yaxis.axis_label = 'Count'
	return p
