from YOUR_API_KEY import key
import requests
import logging
import sys
import os
"""
API request to the Google Maps API

Imputs:
	API key
"""


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

# file_handler = logging.FileHandler('gmap_api.log')
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)

def get_elevations(avglat,avglon):
	locations = str()
	for i, row in enumerate(zip(avglat,avglon)):
		locations += str(avglat[i]) + ',' + str(avglon[i])
		if i < len(avglon) - 1:
		    locations += ' | '

	search_url = 'https://maps.googleapis.com/maps/api/elevation/json?'
	search_payload = {"key": os.environ.get('GOOGLE_API_KEY'),
					 'locations':locations}
	search_req = requests.get(search_url, params=search_payload)
	search_json = search_req.json()
	# logger.debug(search_json)

	results = search_json['results']
	elevations = [i['elevation'] for i in results]

	# if not elevations:
	# 	sys.exit(1)


	return elevations

if __name__ == '__main__':
	print(get_elevations('30.2,-98.8'))