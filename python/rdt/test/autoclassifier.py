import unittest
import rdt.job as job, nltk
from nltk.corpus import stopwords
from rdt.data.mongo.features import Features
from nltk.classify import PositiveNaiveBayesClassifier
from rdt.job import AnnotatedSource

class AutoClassifierTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.ft_db = Features(host='localhost',port=27017,database="reddit_stream",collection="features")
		self.source = AnnotatedSource(host="localhost",port=27017,database="reddit_stream",collection="big_combined")
	def tearDown(self):	
		pass

	def test_classifier(self):
		bgram_doc = list(self.ft_db.find({"subreddit" : "UkrainianConflict"},to_tuples=True,field="bigrams"))[0]
		allbgram_doc = list(self.ft_db.find({"subreddit" : "all"}, to_tuples=True, field='bigrams'))[0]

		pos_fts = { d[0]:True for d in bgram_doc["bigrams"] }
		neu_fts = { d[0]:True for d in allbgram_doc["bigrams"] }
		
		ukr = []
		neu = []

		for doc, fts in self.source.find_ft({"subreddit" : "UkrainianConflict"}):
			nomore = []
			for key in fts.keys():
				if key not in pos_fts:
					nomore = []
				for n in nomore:
					del fts[n]
			if len(fts.keys()) > 0:
				ukr.append(fts)

		for doc, fts in self.source.find_ft(limit=6000):
			neu.append(fts)

		nvb = PositiveNaiveBayesClassifier.train(ukr,neu)
		for do, fts in self.source.find_ft(skip=6000,limit=10):
			print(nvb.classify(fts))
		nvb.show_most_informative_features()

		"""ukr = []
								neu = []
						
								for doc, fts in self.source.find_ft({"subreddit" : "UkrainianConflict"}):
									nomore = []
									for key in fts.keys():
										if key not in pos_fts:
											nomore = []
										for n in nomore:
											del fts[n]
									if len(fts.keys()) > 0:
										ukr.append(fts)
						
								for doc, fts in self.source.find_ft(limit=6000):
									neu.append(fts)
						
								nvb = PositiveNaiveBayesClassifier.train(ukr,neu)
								for do, fts in self.source.find_ft(skip=6000,limit=10):
									print(nvb.classify(fts))
								nvb.show_most_informative_features()"""