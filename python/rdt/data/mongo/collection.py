import pymongo

class Collection(object):
	def __init__(self,	host="localhost",
						port=27017,
						database="reddit_stream_test",
						collection="combined"):
		"""Generalizes pymongo collections. It sets some useful defaults. If
		any necessary short-cuts for mongodb collections come about, then they
		will go here.

		:param host: The hostname of the mongodb database.
		:type host: str
		:param port: The port for the mongodb database.
		:type port: int
		:param database: The mongodb database to connect to.
		:type database: str
		:param collection: The collection to access.
		:type collection: str

		"""
		self.client = pymongo.MongoClient(host=host, port=port)
		self.database = self.client[database]
		self.collection = self.database[collection]
		
		
		self.drop = self.collection.drop

	def find(self,*args,**kwargs):
		return self.collection.find(*args,**kwargs)

	def find_one(self,*args,**kwargs):
		return self.collection.find_one(*args,**kwargs)

	def insert(self,*args,**kwargs):
		return self.collection.insert(*args,**kwargs)
		
	def upsert(self,params=None,doc=None):
		"""Shortcut to mongodb update/upsert. The second parameter to update is:
		{"$set" : doc } .

		:param params: The matching condition for the document to update
		:type params: dict
		:param doc: The value of the "$set" parameter in collection.update
		:type doc: dict
		:returns: A dict describing the effect of the update or None if write acknowledgement is disabled

		"""

		if None in [params,doc]:
			raise UpsertParameters()
		return self.collection.update(
			params,
			{"$set" : doc},
			upsert=True,
			multi=False)
