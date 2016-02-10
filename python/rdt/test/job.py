import unittest
import rdt.job as job, nltk
from nltk.corpus import stopwords

class AnnotatedSourceTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance
		self.job = job.AnnotatedSource(host="localhost",port=27017,database="reddit_stream",collection="big_combined")
	def tearDown(self):	
		pass

	def test_job(self):
		for ind, word in enumerate(self.job.to_words({"subreddit" : "UkrainianConflict"},remove_stopwords=True)):
			# print(word)
			if ind == 20:
				break

	def test_collocation(self):
		gen = self.job.to_words({"subreddit" : "UkrainianConflict"}, remove_stopwords=True)
		finder = self.job.bigram_collocation_finder(gen)
		finder.apply_freq_filter(4)
		finder.apply_word_filter(lambda w: w in stopwords.words('english') + ['-','https', '%','[', ']', "''", "``",'--', "'s", ",", ".","-","(",")",":","n't", "?","!"])
		bigram_measures = nltk.collocations.BigramAssocMeasures()
#		print(finder.nbest(bigram_measures.pmi, 20))
		scored = finder.score_ngrams(bigram_measures.raw_freq)
		print(sorted(finder.ngram_fd.items(), key=lambda t:(-t[1], t[0]))[:10])
		# print(len(finder.ngram_fd.items()))
		# print(sorted(bigram for bigram, score in scored))