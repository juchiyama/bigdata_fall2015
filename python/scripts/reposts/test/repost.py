import unittest, scripts.reposts.nvb as nvb, random, nltk
class RepostTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		docs = nvb.get_reposts()
		random.seed(1)
		random.shuffle(docs)
		featuresets = [(nvb.apply_features(doc), what_is) for (doc,what_is) in docs]
		self.train_set, self.test_set = featuresets[0:int(len(featuresets)/2)], featuresets[int(len(featuresets)/2) + 1:]
		self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
	def tearDown(self):
		pass

	def test_trivial(self):
		print()

		print("Accuracy",nltk.classify.accuracy(self.classifier, self.test_set))
		self.classifier.show_most_informative_features()		

if __name__ == '__main__':
	other = unittest.TestLoader().loadTestsFromTestCase(RepostTestCase)
	derg = unittest.TextTestRunner(verbosity=2).run(other)