import unittest, sys, random, nltk, json
import rdt.data.mongo.source as source
import rdt.nlp.classifier as cls
from nltk import NaiveBayesClassifier
import rdt.nlp.ngrams as ngrams

class ClassifierTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.source = source.Source(host="localhost",port=27017,database="reddit_stream",collection="combined")
	def tearDown(self):
		pass

	def test_features(self):
		"""tests bag of words features
		It appears to work well
		"""
		docs = self.source.find_clean(batch_size=1000)
		for ind, doc in enumerate(docs):
			print(cls.feature(doc))
			if ind == 1:
				break

	def test_classifier(self):
		positive = self.source.find_clean({"subreddit" : "UkrainianConflict"}, limit=2500, batch_size=1000)
		other = self.source.find_clean(limit=2500,batch_size=1000)
		classifier = cls.positive_naive_bayes(positive,other)
		news = self.source.find_clean({"subreddit" : "news"}, limit=10)
		f = open("./UkrainianConflict", "w")
		for doc in news:
			del (doc["_id"])
			truthiness = False
			truthiness = classifier.classify(cls.feature(doc))
			if truthiness:
				f.write(json.dumps(doc) + "\n")
		f.close()
		classifier.show_most_informative_features()

	def test_evaluate(self):
		ukr = self.source.find_clean({"subreddit" : "UkrainianConflict"}, limit=2500, batch_size=1000)
		askr = self.source.find_clean({"subreddit" : "AskReddit"}, limit=2500, batch_size=1000)
		
		alll = self.source.find_clean(limit=10000)
		featuresets = [(cls.feature(doc), "YES") for doc in ukr]
		featuresets.extend([(cls.feature(doc), "NO") for doc in askr])
		random.shuffle(featuresets)
		trainset, testset = featuresets[1250:], featuresets[:1250]
		classifier = NaiveBayesClassifier.train(trainset)
		f = open("./UkrainianConflictNVM","w")
		for doc in alll:
			del (doc["_id"])
			truthiness = False
			truthiness = classifier.classify(cls.feature(doc))
			if truthiness:
				f.write(json.dumps(doc) + "\n")
		f.close()
		print(nltk.classify.accuracy(classifier, testset))