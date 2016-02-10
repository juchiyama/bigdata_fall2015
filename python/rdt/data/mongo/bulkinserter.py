import rdt.data.mongo.source as source
class BulkInserter(object):

	def __init__(self,*args,source=source.Source(host="localhost",port=27017,database="test",collection="test"),size=1000,**kwargs):
		self.source = source
		self.buf = []
		self.size = size
		self.count = 0

	def __enter__(self):
		return self

	def insert(self,item=None):
		self.count += 1
		if item is not None:
			self.buf.append(item)
		if self.count % self.size == 0:
			self.source.insert(self.buf)
			self.buf = []
		if item is None and self.buf:
			self.source.insert(self.buf)

	def send(self):
		self.insert(item=None)
	
	def __exit__(self,type,value,traceback):
		self.insert()
