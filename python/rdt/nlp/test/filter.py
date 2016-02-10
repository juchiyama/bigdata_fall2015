import unittest, sys, rdt.data.clean.html as clean
import rdt.nlp.chunk as chunk, rdt.data.mongo.source as source

def clean_text_iter(docs):
	for d in docs:
		yield d["cleansed_text"]

class FilterTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(conf_key="source_test")
	def tearDown(self):
		pass

	def test_filter(self):
		pass