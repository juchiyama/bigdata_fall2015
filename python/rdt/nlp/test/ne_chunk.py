import unittest, rdt.data.clean.html as clean_html, sys
import rdt.nlp.pos as pos, rdt.data.mongo.source as source
import rdt.nlp.ngrams as ngrams
from nltk.chunk import ne_chunk_sents, ne_chunk
import itertools
import nltk.chunk.util as chunk_tool
from nltk.chunk.util import tree2conlltags

class NEChunkTestCase(unittest.TestCase):

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
		for ind, doc in enumerate(clean_html.doc_iter(docs)):
			sentences = pos.tokenize_sents(doc["cleansed_text"])
			tags = pos.tokenize_words(sentences)
			for sent in tags:
				tagged_sent = tagger.tag(sent)
				d = ne_chunk(tagged_sent)
				chunks = tree2conlltags(d)
				print(chunks)
			if ind == 10:
				break