import rdt.data.mongo.collection as collection
import rdt.conf.data.mongo as conf, os, pymongo
import rdt.data.clean.html as clean

class Source(collection.Collection):
	def __init__(self,*args,**kwargs):
		"""
		:param conf_key: The nltkconf key to use
		:type conf_key: str
		"""
		collection.Collection.__init__(self,*args,**kwargs)

	def most_recent(self,params={}):
		"""This method returns the most recent document.

		:param params: pymongo find parameters
		:type params: dict
		:returns: dict

		"""
		return self.find(params,sort=[("created_utc" , pymongo.DESCENDING)])[0]
		
	def most_recent_created_utc(self,params={}):
		"""This method returns the most recent created_tuc value.

		:param params: pymongo find parameters
		:type params: dict
		:returns: int

		"""
		return self.most_recent(params)["created_utc"]

	def find_clean(self,*args,**kwargs):
		"""This functions just like normal find, but cleans the documents at the same time
		"""

		batch_size = kwargs["batch_size"] if "batch_size" in kwargs else 100

		docs = self.find(*args,**kwargs)
		docs.batch_size(batch_size)
		if "skip_none" in kwargs and kwargs["skip_none"] is True:
			return clean.skip_iter(docs)
		else:
			return clean.doc_iter(docs)