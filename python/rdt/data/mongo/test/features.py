import unittest, html
from rdt.data.mongo.features import Features
import rdt.data.clean.html as clean_html


class FeaturesDBTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.fts_db = Features(host="localhost",port=27017,database="reddit_stream",collection="features")
	def tearDown(self):	
		pass

	def test_convert_list_to_tuples(self):
		for doc in self.fts_db.find({"subreddit" : "UkrainianConflict"}, to_tuples=True,field="bigrams"):
		 	print(doc)
		