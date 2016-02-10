import re

def get_ne(sentence):
	""" For a list of (word, parts of speech, BIO) tuples, 
	return each instance of a named entity.

	:param sentence: A list of (word,pos,BIO) tuples
	:type sentence: (str,str,str)
	"""
	if not sentence:
		return []
	if type(sentence[0]) is list:
		return [_get_ne(sent) for sent in sentence]
	else:
		return _get_ne(sentence)

def _get_ne(sentence):
	_b = re.compile("^B")
	_i = re.compile("^I")
	ne = []
	for tup in sentence:
		# add a new tuple or NE
		if _b.search(tup[2]):
			ne.append([tup])
		# add to the most recent B or I tag
		# the additional NE information
		if _i.search(tup[2]):
			ne[-1].append(tup)
	return ne

def get_nouns(sentence):
	"""  For either a list of sentences, or a single sentence
	return the list of noun word forms found within.

	:param sentence: list of list of strings or list of strings
	:type sentence: [[str]] or [str]
	
	"""
	if not sentence:
		return []
	nouns = []
	if type(sentence[0]) is list:
		for sent in sentence:
			nouns.extend(_get_nouns(sent))
		return nouns
	else:
		return _get_nouns(sentence)

def _get_nouns(sentence):
	_n = re.compile("^NN")
	nouns = []
	for sent in sentence:
		if _n.search(sent[1]):
			nouns.append(sent[0])
	return nouns