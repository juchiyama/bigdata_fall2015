import unittest
import rdt.data.mongo.source as source
import rdt.data.clean.html as clean_html
import rdt.data.normalize as normalize

class NormalizeTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(conf_key="source_test")
	def tearDown(self):	
		pass

	def test_small_corpus(self):
		docs = self.source.find()
		docs.batch_size(10000)
		for ind, doc in enumerate(clean_html.doc_iter(docs)):
			print(normalize.post(doc))
			if ind == 10: break
