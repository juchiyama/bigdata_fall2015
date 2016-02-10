import unittest, sys, rdt.data.clean.html as clean
import rdt.nlp.chunk as chunk, rdt.data.mongo.source as source
import rdt.nlp.corpus.annotate as annotate
import rdt.nlp.ngrams as ngrams
import rdt.nlp.classifier as cls

class PNBAnnotateTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(host="localhost",port=27017,database="reddit_stream",collection="combined")
	def tearDown(self):
		pass

	def test_classbased(self):
		tagger = ngrams.make_backoff_tagger()
		params = {
			"corpora" : self.source,
			"labeled_set" : lambda : self.source.find_clean({"subreddit" : "fitness"}, batch_size=1000, limit=2000),
			"unlabeled_set" : lambda : self.source.find_clean({"subreddit" : "AskReddit"}, batch_size=1000, limit=2000),
			"feature" : lambda x : cls.ner_feature(x,tagger=tagger),
			"exit" : lambda self : self.corpora.exit()
		}

		pnb_a = annotate.PNBAnnotater(**params)
		pnb_a.train()
		pnb_a.describe()
		ct = 0
		for doc, annotation in pnb_a.classify_iter(self.source.find_clean()):
			ct += 1
			# print(doc)
			print(annotation)
			if ct == 10:
				break
			print("------------")