import unittest, re, string, nltk, json, rdt.mr.annotation as annotation
from rdt.data.mongo.bulkinserter import BulkInserter
from rdt.data.mongo.source import Source

class KeyFixTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.inserter = BulkInserter(host="localhost",port=27017,database="reddit_stream_test",collection="users")
	def tearDown(self):	
		self.inserter.source.drop()

	def test_keyfix_characters(self):
		count = 0
		for ind, user in enumerate(annotation.user_reader("data/test_key.json")):
			self.inserter.insert(item=user)
			count = ind
		self.inserter.send()
		count_2 = 0
		for ind, user in enumerate(self.inserter.source.find()):
			count_2 = ind
		self.t(count == count_2)

def main():
	suite = lambda x : unittest.TestLoader().loadTestsFromTestCase(x)
	runner = lambda x : unittest.TextTestRunner(verbosity=2).run(x)
	run = lambda x : runner(suite(x))
	return run(KeyFixTestCase)