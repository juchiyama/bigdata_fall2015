import unittest, sys, rdt.data.clean.html as clean
import rdt.nlp.chunk as chunk, rdt.data.mongo.source as source

def clean_text_iter(docs):
	for d in docs:
		yield d["cleansed_text"]

class UnigramTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(conf_key="source_test")
	def tearDown(self):
		pass

	def test_unigram(self):
		docs = self.source.find()
		docs.batch_size(1000)
		docs = clean.doc_iter(docs)
		for ind, doc in enumerate(chunk.simple_np_ugram([d["cleansed_text"] for d in docs])):
			print(doc)
			if ind == 2:
				break

	def test_bigram(self):
		docs = self.source.find()
		docs.batch_size(1000)
		docs = clean.doc_iter(docs)
		for ind, doc in enumerate(chunk.simple_np_bgram([d["cleansed_text"] for d in docs])):
			print(doc)
			if ind == 2:
				break