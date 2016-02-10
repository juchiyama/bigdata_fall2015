from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords
import rdt.nlp.pos as pos
from nltk.corpus import stopwords
from nltk.tag.sequential import BigramTagger, TrigramTagger, DefaultTagger, UnigramTagger
import itertools
from nltk.corpus import treebank
from nltk.tag import SequentialBackoffTagger
from nltk.corpus import names

def collocationFinder(document,nbest=4):
	""" The is a bigram collocation finder. 
	:param document:
	"""
	chain = lambda x : list(itertools.chain(*pos.tokenize_words(pos.tokenize_sents(x))))
	stopset = set(stopwords.words('english'))
	filter_stops = lambda w: len(w) < 3 or w in stopset
	bcf = BigramCollocationFinder.from_words(chain(document))
	bcf.apply_word_filter(filter_stops)
	return bcf.nbest(BigramAssocMeasures.likelihood_ratio, 4)

def backoff_tagger(train_sents, tagger_classes, backoff=None):
	""" Given a set of tagger_class and conll2000 training sentences,
	this function returns a good backoff POS tagger. 

	"""
	for cls in tagger_classes:
		backoff = cls(train_sents,backoff=backoff)
	return backoff

def make_backoff_tagger():
	""" Returns a backoff tagger that useses a UnigramTagger,
	BigramTagger, TrigramTagger, and a Default tagger that returns NN

	:returns: A backoff POS tagger.

	"""

	return backoff_tagger(treebank.tagged_sents(), 
		[UnigramTagger, BigramTagger, TrigramTagger],
		backoff=DefaultTagger('NN'))

class NamesTagger(SequentialBackoffTagger):
	def __init__(self, *args, **kwargs):
		SequentialBackoffTagger.__init__(self, *args, **kwargs)
		self.name_set = set([n.lower() for n in names.words()])

		""" From the names in nltk.corpus, this looks up names in a 
		dictionary. If found, returns NNP. This class inherits 
		from SequentialBackoffTagger

		"""

	def choose_tag(self, tokens, index, history):
		word = tokens[index]
		if word.lower() in self.name_set:
			return 'NNP'
		else:
			return None
