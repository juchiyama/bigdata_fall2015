import unittest, rdt.data.clean.html as clean_html, sys
import rdt.nlp.pos as pos, rdt.data.mongo.source as source
import rdt.nlp.ngrams as ngrams
from nltk.chunk import ne_chunk_sents, ne_chunk
import itertools
import nltk.chunk.util as chunk_tool
from nltk.chunk.util import tree2conlltags
import rdt.nlp.conll_get as cnll

class ConllGetTestCase(unittest.TestCase):

	"""This would likely be very good for user summarization
	and categorization"""

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(host="localhost",port=27017,database="reddit_stream_test",collection="combined")
	def tearDown(self):
		pass

	def test_interactive(self):
		docs = self.source.find_clean(batch_size=1000)
		tagger = ngrams.make_backoff_tagger()
		print()
		for ind, doc in docs:
			sentences = pos.tokenize_sents(doc["cleansed_text"])
			tags = pos.tokenize_words(sentences)
			for sent in tags:
				tagged_sent = tagger.tag(sent)
				d = ne_chunk(tagged_sent)
				chunks = tree2conlltags(d)
				print("CHUNKS" + str(chunks))
				print("NE"+str(cnll.get_ne(chunks)))
				print("NOUNS"+str(cnll.get_nouns(chunks)))
			if ind == 10:
				break
