import ConfigParser
class Config:
	"""
	Info of config.ini
	"""
	def __init_(self,path):
		self.path = path
		self.cf = ConfigParSer.ConfigParser()
		self.cf.read(self.path)
	def get(self,field,key):
		result = ""
		try:
			result = self.cf.get(field,key)
		except:
			result = ""
		return result
	def set(self,field,key,value):
		try:
			self.cf.set(field,key,value)
			cf.write(open(self.path,'w'))
		except:
			return False
		return True
def read_config(config_file_path,field,key):
	cf = ConfigParser.ConfigParser()
	try:
		cf.read(config_file_path)
		result = cf.get(field,key)
	except:
		sys.exit(1)
	return result
