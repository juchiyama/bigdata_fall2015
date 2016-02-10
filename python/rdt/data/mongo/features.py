import rdt.data.mongo.collection as collection
import rdt.conf.data.mongo as conf, os, pymongo
import rdt.data.clean.html as clean

class Features(collection.Collection):
	def __init__(self,*args,**kwargs):
		"""
		:param conf_key: The nltkconf key to use
		:type conf_key: str
		"""
		collection.Collection.__init__(self,*args,**kwargs)

	def _to_tuples(self,field="bigrams",docs=[]):
		for doc in docs:
			bgrams = doc[field]
			bgrams = [ ((b[0][0], b[0][1]),b[1]) for b in bgrams]
			doc[field] = bgrams
			yield doc


	def find(self,*args,to_tuples=False,field="bigrams",**kwargs):
		"""MongoDB doesn't store tuples, so we have a way to convert 
		[[word1,word2],count] to ((word1,word2),count)
		Note: The parameter specification is given to change.

		:param to_tuples: Causes the to_tuples conversion
		:type to_tuples: bool

		:param field: Determines what field the tuples exist in
		:type field: str

		"""

		if to_tuples:
			return self._to_tuples(field=field,docs=super(Features, self).find(*args,**kwargs))
		else:
			return super().find(*args,**kwargs)

	def restrict(self, refset, other):
		pass