import unittest, html
import rdt.data.mongo.source as source
import rdt.data.clean.html as clean_html

class CleanHTMLTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(host="localhost",port=27017,database="reddit_stream_test",collection="test")
	def tearDown(self):	
		pass

	def test_small_corpus(self):
		print(self.source.most_recent_created_utc())
		count = 0
		docs = self.source.find()
		docs.batch_size(10000)
		for ind, doc in enumerate(clean_html.doc_iter(docs)):
			print(doc["cleansed_text"])
			print("VS")
			print(self.body_or_selftext(doc))
			print("----------")

	def body_or_selftext(self,doc):
		if "selftext" in doc:
			return doc["selftext"]
		else:
			return doc["body"]