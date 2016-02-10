import unittest, sys, rdt.data.clean.html as clean
import rdt.nlp.chunk as chunk
from rdt.data.mongo.features import Features
from rdt.job import AnnotatedSource
import random, nltk

def feature(doc,bg):
	pass

class SubredditClassifierTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.feature = Features(host="localhost",port=27017,database="reddit_stream",collection="features")
		self.source = AnnotatedSource(host="localhost",port=27017,database="reddit_stream",collection="big_combined")
	def tearDown(self):
		pass

	def test_bigram(self):
		bg = list(self.feature.find({"subreddit" : "UkrainianConflict"}, to_tuples=True,field="bigrams"))[0]
		bg = [ d[0] for d in bg["bigrams"] ]
		words = [d[0] for d in bg]
		words.extend([d[1] for d in bg])
		words = list(set(words))
		# print(words)
		# print(bg)
		yay = []
		for doc, ft in self.source.find_ft({"subreddit" : "UkrainianConflict"},batch_size=1000):
			tups = ft.keys()
			the_words = list(set([d[0] for d in tups] + [d[1] for d in tups]))
			# is identifying words in the_words
			for word in words:
				ft["contains(" + word + ")"] = word in the_words
			to_dump = []
			for key in ft.keys():
				if key not in bg:
					to_dump.append(key)
			for dump in to_dump:
				del ft[dump]
			if len(ft.keys()) > 0:
				yay.append((ft,"UkrainianConflict"))
			#print()
			#print(bg)
		for doc, ft in self.source.find_ft({}, limit=6000,batch_size=1000):
			yay.append((ft, "Not UkrainianConflict"))

		random.shuffle(yay)
		test_set, train_set = yay[int(len(yay)/2):], yay[:int(len(yay)/2)]
		classifier = nltk.NaiveBayesClassifier.train(train_set)

		classifier.show_most_informative_features()

		for doc, ft in self.source.find_ft({"subreddit" : "news"}, skip=6000,batch_size=1000):
			if classifier.classify(ft) == "UkrainianConflict":
				print("YAY", doc)