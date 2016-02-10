import nltk

"""
This encapsulates basic nltk processes.

"""

def preprocess(document):
	"""	
		This tokenizes a string into sentences.
		After sentence tokenization, the sentences are word tokenized.
		After word tokenization, the words receive POS tagging.
		Each of these methods use nltk-native methods.

		:param document: The string containing many sentences to parse.
		:type document: str.
		:returns: array[array[(word, pos)]]
	"""
	sentences = tokenize_sents(document)
	#print "\n"
	#print sentences, "\n"
	sentences = tokenize_words(sentences)
	#print sentences, "\n"
	sentences = pos_tag_sentences(sentences)
	#print sentences, "\n"
	return sentences

def pos_tag_sentences(sentences):
	"""

	:param sentences: [["word","word"]]
	:type sentences: [[str]]
	:returns: [[(word,pos)]]

	"""
	return [nltk.pos_tag(sent) for sent in sentences]

def tokenize_words(sentences):
	"""

	:param sentences: ["The dog ate the rock"]
	:type sentences: array(str)
	:returns: [["The","dog","ate","the","rock"]]

	"""
	return [nltk.word_tokenize(sent) for sent in sentences]

def tokenize_sents(document):
	"""
	:param document: A string containing many sentences
	:type document:  str
	:returns: An array of sentence strings. [str]

	"""

	return nltk.sent_tokenize(document)
"""
	[[(word, pos), (word, pos)]]
"""

def list_to_tuples(sentence):
	"""
		Mongodb stores tuples as arrays.
		This converts the arrays back to tuples.
	"""

	sub = []
	for d in sentence:
		sub.append((d[0],d[1]))
	return sub

def list_list_to_tuples(sentences):
	return [list_to_tuples(d) for d in sentences]

def np_pp_vp_class(pos_sentences):
	"""
		:param pos_setences: Parts of speech tagged sentences
		:type pos_sentences: array[array]
		:returns: array of POS tagged sentences

	"""

	grammar = r"""
		NP: {<DT|JJ|NN.*>+}
		PP:{<IN><NP>}
		VP:{<VB.*><NP|PP|CLAUSE>+$}
		CLAUSE: {<NP><VP>}
		"""
	cp = nltk.RegexpParser(grammar)
	my_return = []
	for sentence in pos_sentences:
		my_return.append(cp.parse(sentence))
	return my_return

def pos_features(sentence, i, history):
	"""This is used as a part of the ConsecutivePosTagger.
	For a position in a sentence, returns a set of features
	containing the one letter, two letter, and three letter suffixes
	of the current word. It also tracks eatures for the 
	previous wordform and tag. 


	"""

	features = {"suffix(1)" : sentence[i][-1:],
				"suffix(2)" : sentence[i][-2],
				"suffix(3)" : sentence[i][-3]}
	if i == 0:
		features['prev-word'] = "<START>"
		features['prev-tag'] = "START"
	else:
		features['prev-word'] = sentence[i-1]
		features['prev-tag'] = history['i-1']
	return features

"""
	This is an nlp-text book example
	its missing something...

"""

class ConsecutivePosTagger(nltk.TaggerI):
	""" Tags parts of speech based upon the previous
	word's tag. It uses a naive bayes classifier.

	"""

	def __init__(self, train_sents):
		""" For the tagged [[(word, pos)]] sentences 
		in the training set, determine the parts of speech features
		for the each word in the sentence. Relate a feature 
		set to a tag and record the sequential position of that 
		parts of speech tag. Run this through a NaiveBayesClassifier

		"""
		train_set = []
		for tagged_sent in train_sents:
			untagged_sent = nltk.tag.untag(tagged_sent)
			history = []
			for i, (word,tag) in enumerate(tagged_sent):
				featureset = pos_features(untagged_sent, i, history)
				train_set.append((featureset, tag))
				history.append(tag)
		self.classifier = nltk.NaiveBayesClassifier.train(train_set)

	def tag(self, sentence):
		""" Apply parts of speech tags to a tokenized list of words.
		"""

		history = []
		for i, word in enumerate(sentence):
			featureset = pos_features(sentence,i,history)
			tag = self.classifier.classify(featureset)
			history.append(tag)
		return zip(sentence,history)