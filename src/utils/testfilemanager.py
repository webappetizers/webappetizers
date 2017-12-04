import filemanager

elevations = [111,2,13]
# Save to file
try:
	manager = filemanager.Manager('elevations', '.csv',elevations,'a')
	manager.write()
except Exception as e:
	print(e)