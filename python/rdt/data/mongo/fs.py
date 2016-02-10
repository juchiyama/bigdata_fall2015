import pymongo

class FileSystem(object):

	def __init__(self,*args,**kwargs):
		self.port = kwargs["port"]
		self.host = kwargs["host"]
		self.client = pymongo.MongoClient(self.host,self.port)