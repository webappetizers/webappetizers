import json
import pandas as pd
from .filemanager import Manager
from .gmap_api import get_elevations


def lines():
	file = 'data/austin_texas_osm_line.geojson'
	file2 = 'austin_texas_osm_line.geojson'

	try:
		with open(file, encoding='utf8') as f:
			lines = json.load(f)
			return lines
	except Exception as e:
		print(e)
		return {}

def split_points(line):
	"""
	Accepts a StringLine consecutive coordinates 
	and splits each segment into its own unique
	line record

	Input: [[lat1,lon1] , [lat2,lon2] , ... ]
	Output: DataFrame
	"""
	
	df = pd.DataFrame()
	df['lat1'] = [line[i][1] for i in range(0,len(line)-1)]
	df['lon1'] = [line[i][0] for i in range(0,len(line)-1)]
	df['lat2'] = [line[i+1][1] for i in range(0,len(line)-1)]
	df['lon2'] = [line[i+1][0] for i in range(0,len(line)-1)]

	return df

def data():
	l = lines()
	df = pd.DataFrame()

	for i,feature in enumerate(l['features']):
		line = feature['geometry']['coordinates']
		df = df.append(split_points(line), ignore_index=True)
		
		if i ==1:
			break

	df['avgLat'] = df[['lat1','lat2']].mean(axis=1)
	df['avgLon'] = df[['lon1','lon2']].mean(axis=1)

	locations = str()
	elevations = []
	for index, row in df.iterrows():
		locations += str(row['avgLat']) + ',' + str(row['avgLon'])
		# if index < df.shape[0] - 1:
		#     locations += ' | '

		elevations += [index]
		
	# elevations = get_elevations(locations)

	# Save to file
	df.to_pickle('coords')
	try:
		manager = filemanager.Manager('elevations', '.csv',elevations,'a')
		manager.write()
	except Exception as e:
		print(e)

	mydata = {
		'lon': [[df['lon1'][i], df['lon2'][i]] for i, row in df.iterrows()],
		'lat': [[df['lat1'][i], df['lat2'][i]] for i, row in df.iterrows()],
		'elev': elevations,
	}
	return mydata

if __name__ == '__main__':
	print(data())