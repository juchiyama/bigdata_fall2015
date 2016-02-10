import unittest, rdt.data.clean.html as clean_html, sys
import rdt.nlp.pos as pos, rdt.data.mongo.source as source

class CleanHTMLTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(conf_key="source_test")
	def tearDown(self):
		pass

	def test_interactive(self):
		docs = self.source.find()
		docs.batch_size(1000)
		for ind, doc in enumerate(clean_html.doc_iter(docs)):
			new_doc = pos.preprocess(doc["cleansed_text"])
			print(new_doc)
			break