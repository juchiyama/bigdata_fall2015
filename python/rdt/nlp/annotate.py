import rdt.data.clean.html as clean
import rdt.data.mongo.source as rdtcorp
import rdt.nlp.ngrams as ngrams
import rdt.nlp.pos as pos
from nltk.chunk import ne_chunk
from nltk.chunk.util import tree2conlltags
import rdt.nlp.conll_get as cnll
import rdt.data.clean.html as html
import json, nltk

def dirty_dict(doc,tagger=None):
	""" Make clean a dictionary and annotate.

	:param doc: A dictionary without cleansed_text added
	:type doc: dict

	:param tagger: A pos tagger. 
	:type tagger: Tagger

	:returns: dict
	"""

	return clean_dict(html.clean_doc(doc),tagger=tagger)

def dirty_dicts(docs,tagger=None):
	""" Make clean many dictionaries and annotate.
	
	:param docs: Dictionaries without cleansed_text.
	:type docs: [{docs}]

	:param tagger: A pos tagger. 
	:type tagger: Tagger

	:returns: generator(dict)
	"""
	for doc in docs:
		yield dirty_dict(doc, tagger=tagger)
	
def clean_dict(doc,tagger=nltk.pos_tag):
	""" Processes NLP features from cleansed_text. All other functions
	wrap this one. 
	Serves to act as the NLP-front end for reddit corpus
	parsing. Dictionaries and json strings are accepted and return
	dictionaries containing additional information. The processing
	done here represents the general annotations. The following
	are the new fields added to the dictionary. Classifiers
	will work to modify or wrap these methods. 

	::

		{
			conlltags 		: [[(word, pos, BIO)]],
			nouns 			: [word],
			named_entities 		: [[word, pos, BIO]],
			cleansed_text 		: [[word]]
		}

	:param doc: dictionary of reddit corpus.
	:type doc: dict

	:param tagger: A pos tagger. 
	:type tagger: Tagger

	:returns: dict
	"""

	if "_id" in doc: del(doc["_id"])
	sentences = pos.tokenize_sents(doc["cleansed_text"])
	tags = pos.tokenize_words(sentences) or []
	doc["conlltags"] = []
	doc["nouns"] = []
	doc["named_entities"] = []
	for sent in tags:
		tagged_sent = nltk.pos_tag(sent) or []
		d = ne_chunk(tagged_sent) or []
		chunks = tree2conlltags(d)
		doc["conlltags"].append(chunks)
		doc["nouns"].extend(cnll.get_nouns(chunks))
		doc["named_entities"].extend(cnll.get_ne(chunks))
	return doc

def clean_dicts(docs,tagger=None):
	""" Returns the annotated version of the document. 

	:param docs: Dictionarie to be annotated:
	:type docs: [{}]

	:param tagger: A pos tagger. 
	:type tagger: Tagger

	:returns: iter([dict])
	"""
	for doc in enumerate(docs):
		yield clean_dict(doc,tagger=tagger)

def dirty_json(doc,tagger=None):
	""" Returns the annotated and clean version of the document.

	:param doc: json string without cleansed text or annotations
	:type doc: str

	:param tagger: A pos tagger. 
	:type tagger: Tagger

	:returns: dict
	"""
	return clean_dict(html.clean_doc(json.loads(doc)),tagger=tagger)
	
def dirty_jsons(docs,tagger=None):
	""" Returns the annotated and clean versions of the documents.

	:param docs: List of unannotated json strings
	:type docs: ["{json_string}"]

	:param tagger: A pos tagger. 
	:type tagger: Tagger

	:returns: generator(dict)
	"""
	for doc in docs:
		yield dirty_json(doc,tagger=tagger)

def clean_json(doc,tagger=None):
	"""	Returns the annotated form of the json document. 

	:param doc: A dictionary with cleansed_text
	:type doc: str

	:param tagger: A pos tagger. 
	:type tagger: Tagger

	:returns: dict
	"""
	return clean_dict(json.loads(doc),tagger=tagger)

def clean_jsons(docs,tagger=None):
	""" Returns the annotated form of the json documents.

	:param docs: list of json documents containing cleansed_text fields
	:type docs: [str]

	:param tagger: A pos tagger. 
	:type tagger: Tagger
	:returns: iter([dict])
	"""
	for doc in docs:
		yield clean_json(doc,tagger=tagger)