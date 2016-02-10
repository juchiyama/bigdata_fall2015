import unittest, rdt.data.clean.html as clean_html, sys
import rdt.nlp.pos as pos, rdt.data.mongo.source as source
import rdt.nlp.ngrams as ngrams
import itertools

class BackOffTestCase(unittest.TestCase):

	"""This would likely be very good for user summarization
	and categorization"""

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(conf_key="source_test")
	def tearDown(self):
		pass

	def test_interactive(self):
		docs = self.source.find()
		docs.batch_size(1000)
		tagger = ngrams.make_backoff_tagger()
		chain = lambda x : list(itertools.chain(*pos.tokenize_words(pos.tokenize_sents(x))))
		for ind, doc in enumerate(clean_html.doc_iter(docs)):
			print(tagger.tag(chain(doc["cleansed_text"])))
			if ind == 10:
				break