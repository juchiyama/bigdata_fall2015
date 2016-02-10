import unittest, sys, rdt.data.clean.html as clean, json
import rdt.nlp.chunk as chunk, rdt.data.mongo.source as source
import rdt.nlp.ngrams as tagger, rdt.nlp.annotate as annotate

class AnnotateTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(host="localhost",port=27017,database="reddit_stream_test",collection="combined")
		self.tagger = tagger.make_backoff_tagger()
	def tearDown(self):
		pass

	def test_unigram(self):
		docs = self.source.find()
		docs.batch_size(1000)
		
		for ind, doc in enumerate(annotate.dirty_dicts(docs,tagger=self.tagger)):
			print(doc)
			if ind == 10:
				break

		jsons = []
		docs = self.source.find()
		for ind, doc in enumerate(docs):
			del(doc["_id"])
			jsons.append(json.dumps(doc))
			if ind == 10:
				break

		for ind, doc in enumerate(annotate.dirty_jsons(jsons,tagger=self.tagger)):
			print(doc)



