from rdt.data.mongo.source import Source
import rdt.nlp.pos as pos
from nltk.corpus import stopwords
from nltk.classify import PositiveNaiveBayesClassifier
import rdt.nlp.annotate as annotate, rdt.nlp.conll_get as conll_get
import rdt.nlp.ngrams as ngrams

def feature(document):
	"""This builds bag of words features and also adds subreddit as a feature.
	:param document: The dictionary reddit document.
	:type document: dict
	"""
	final = filter_words(document["cleansed_text"])
	return dict(('contains(%s)' % w, True) for w in final)

def ner_feature(document,tagger=None):
	if tagger is None:
		tagger = ngrams.make_backoff_tagger()
	sents = annotate.dirty_dict(document,tagger=tagger)
	fts = {}
	for noun in sents["nouns"]:
		nn = "contains_noun(" + noun + ")"
		fts[nn] = True
	return fts

def filter_words(text):
	"""Prepares the reddit document for bag of words. Turns the text
	into an array of strings, without stopwords
	:param text: blob of text
	:type text: [str]
	"""
	sents = pos.tokenize_words(pos.tokenize_sents(text))
	final = []
	"""turn the list of sentences into a list of words"""
	for sent in sents:
		final.extend(sent)
	stop = stopwords.words('english')
	final = [w for w in final if w.lower() not in stop]
	final = [w.lower() for w in final]
	return final

def subreddit(subreddit=None,batch_size=100):
	if subreddit is None:
		return None
	source = Source(host="localhost",port=27017,database="reddit_stream",collection="combined")
	cursor = source.find_clean({"subreddit" : subreddit},batch_size=batch_size)
	return cursor

"""other = source.find_clean()[:1500]"""
def positive_naive_bayes(pos_cursor,unlabeled_cursor):
	"""send over entire documents"""
	return PositiveNaiveBayesClassifier.train(list(map(feature, pos_cursor)), list(map(feature, unlabeled_cursor)))