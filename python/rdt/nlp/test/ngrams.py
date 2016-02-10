import unittest, rdt.data.clean.html as clean_html, sys
import rdt.nlp.pos as pos, rdt.data.mongo.source as source
import rdt.nlp.ngrams as bigrams

class BigramsTestCase(unittest.TestCase):

	"""This would likely be very good for user summarization
	and categorization"""

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		params = {
			"host":"localhost",
			"port":27017,
			"database":"reddit_stream_test",
			"collection":"combined"
		}

		self.source = source.Source(**params)
	def tearDown(self):
		pass

	def test_interactive(self):
		docs = self.source.find()
		docs.batch_size(1000)
		for ind, doc in enumerate(clean_html.doc_iter(docs)):
			del(doc["_id"])
			dc = bigrams.collocationFinder(doc["cleansed_text"])
			print("\n")
			print(dc)
			break