import os


class Manager():
	def __init__(self, name, ext, data=None, action='r'):
		self.name = name
		self.action = action
		self.data = '\n'.join(str(i) for i in data)
		self.ext = ext
		

	def write(self):
		num = 0		

		f = os.path.isfile('../data/' + self.name + str(num) + self.ext)
		while f == True:
			num +=1
			f = os.path.isfile('../data/' + self.name + str(num) + self.ext)
			
		self.action = 'w' # make a new file if not

		filename = '../data/' + self.name + str(num) + self.ext
		
		with open(filename, self.action) as f:
			f.write(self.data)
	
		return

