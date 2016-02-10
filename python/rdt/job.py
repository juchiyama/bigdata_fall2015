from rdt.data.mongo.source import Source
import rdt.nlp.pos as pos, nltk, itertools
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.classify import PositiveNaiveBayesClassifier

class AnnotatedSource(Source):
	"""This class simplifies some repetitive batch jobs.
	Much of this class is used for short descriptive analysis.

	"""
	def __init__(self,*args,**kwargs):
		"""Send the Source parameters and optionally set soem attributes

		"""
		self._stop_words = stopwords.words('english')
		Source.__init__(self,*args,**kwargs)
		if_def = lambda x: kwargs[x] if x in kwargs else None
		for attr in ["sentence_tokenizer","word_tokenizer"]:
			setattr(self,attr,if_def(attr))
		self.stopwords = stopwords.words('english')
		self.unwanted_strings = ['https', '[', ']', "''", 
			"``",'--', "'s", 
			",", ".","-",
			"(",")",":",
			"n't", "?","!"]

	def _should_strip(self,w):
		return w.lower() in self._stop_words

	def _strip(self,ws):
		for w in ws:
			if not self._should_strip(w):
				yield w


	def words(self,doc,remove_stopwords=False):
		"""Given a reddit dictionary,
		return the words given by the native sentence and
		words tokenizers.

		:param doc: a reddit-document
		:type doc: dict

		"""

		d = pos.tokenize_words(pos.tokenize_sents(doc["cleansed_text"]))
		for a in d:
			if remove_stopwords:
				a = self._strip(a)
			for f in a:
				yield f

	def words_iter(self,docs):
		"""Given many reddit dictonaries, return a flattened generator of words.

		:param docs: generator or list of reddit-documents.
		:type docs: list(dict)

		"""
		for doc in docs:
			for w in self.words(doc):
				yield w

	def to_words(self,condition,remove_stopwords=False,**kwargs):
		"""Given a MongoDB find parameter, return the words of the 
		text containing bodies.

		:param condition: The MongoDB conditions to search
		:type condition: dict

		"""
		gen = self.words_iter(self.find_clean(condition,skip_none=True,**kwargs))
		if remove_stopwords:
			gen = self._strip(gen)

		for word in gen:
			yield word

	def bigram_collocation_finder(self,words):
		return BigramCollocationFinder.from_words(words)

	def bigram_nbest(self,bg,count=10):
		return bg.nbest(nltk.collocations.BigramAssocMeasures().pmi,count)

	# http://streamhacker.com/2010/05/24/text-classification-sentiment-analysis-stopwords-collocations/
	def bigram_word_feats(self,words,n=200):
		bigram_finder = self.bigram_collocation_finder(words)
		bigram_finder.apply_word_filter(lambda w: w in  self.stopwords + self.unwanted_strings)
		bigram_measures = nltk.collocations.BigramAssocMeasures()
		bigrams = sorted(bigram_finder.ngram_fd.items(), key=lambda t:(-t[1], t[0]))
		return {d[0]:True for d in bigrams}

	def find_ft(self,*args,**kwargs):
		for doc in self.find_clean(*args,skip_none=True,**kwargs):
			words = list(self.words(doc))
			yield (doc, self.bigram_word_feats(words ))

	def subreddit_classifier(self,condition,remove_stopwords=False,n=200):
		yes_fts = []
		no_fts = []
		ct = 0
		for ind, doc in enumerate(self.find_clean(condition,skip_none=True)):
			words = list(self.words(doc))
			yes_fts.append(self.bigram_word_feats(words,n=200))
			ct = ind

		for doc in self.find_clean({},skip_none=True,limit=ind):
			words = list(self.words(doc))
			no_fts.append(self.bigram_word_feats(words,n=200))

		return PositiveNaiveBayesClassifier.train(yes_fts,no_fts)