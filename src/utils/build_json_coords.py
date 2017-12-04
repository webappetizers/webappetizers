import json
import pandas as pd
import os


def lines():
	file = 'austin_texas_osm_line.geojson'
	
	try:
		with open(file, encoding='utf8') as f:
			lines = json.load(f)
			print('Acquired lines')
			return lines
	except Exception as e:
		print(e)
		return

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

def coords_list():
	l = lines()
	df = pd.DataFrame()
	total_lines = len(l)
	print (total_lines)

	for i,feature in enumerate(l['features']):
		line = feature['geometry']['coordinates']
		df = df.append(split_points(line), ignore_index=True)
		print('Finished df segment ', i)

		if i == 20:
			break

	coords = []
	for i, line in df.iterrows():
		record = {
			"city": "Austin",
			"coords":
				{
					'lat1':line['lat1'],
					'lon1':line['lon1'],
					'lat2':line['lat2'],
					'lon2':line['lon2']
				}
		}

		coords.append(record)
		print('Record appended to df')
	return coords

def main():
	file = 'test_coords.json'
	# if not os.path.exists(file):
	coords = coords_list()

	with open(file, 'w') as f:
		json.dump(coords, f)

	print('Created coords.json')
	return

if __name__ == '__main__':
	main()
	# df = pd.read_pickle('coords')
	# print(df)