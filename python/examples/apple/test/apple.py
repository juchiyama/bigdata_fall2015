import unittest, examples.apple.nvb as nvb, random, nltk
class AppleTestCase(unittest.TestCase):

	def setUp(self):
		"""redoing stuff because john is stupid"""
		self.t = self.assertTrue
		docs = nvb.get_apples()
		#random.seed(0)
		random.shuffle(docs)
		featuresets = [(nvb.apply_features(doc), what_is) for (doc,what_is) in docs]
		self.train_set, self.test_set = featuresets[len(featuresets)/2:], featuresets[:len(featuresets)/2 + 1]
		self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
	def tearDown(self):
		pass

	def test_trivial(self):
		print()

		print("Accuracy",nltk.classify.accuracy(self.classifier, self.test_set))
		self.classifier.show_most_informative_features()		

if __name__ == '__main__':
	other = unittest.TestLoader().loadTestsFromTestCase(AppleTestCase)
	derg = unittest.TextTestRunner(verbosity=2).run(other)