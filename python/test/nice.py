import unittest, re, string
import nltk
from rdt.data.mongo.source import Source
import rdt.data.clean.html as html

class NiceTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = Source(host="localhost",port=27017,database='reddit_stream_test',collection='combined')
	def tearDown(self):	
		pass

	def test_no_bad_characters(self):
		print("\n")
		remov = re.compile("[0-9]")
		for doc in html.doc_iter(self.source.find().limit(1000)):
			print("".join(list(filter(lambda x : x in string.printable, doc["cleansed_text"]))))

def main():
	suite = lambda x : unittest.TestLoader().loadTestsFromTestCase(x)
	runner = lambda x : unittest.TextTestRunner(verbosity=2).run(x)
	run = lambda x : runner(suite(x))
	return run(NiceTestCase)
