import nltk, re
from pymongo import MongoClient

def apply_features(doc):
	features = {}
	features['regex(apple)'] = bareword_match('(^|\s)(A|a)pple((\')?s)?(\s|$)',_get_text(doc))
	features['regex(macintosh)'] = bareword_match('\W(M|m)ac(intosh)?((\')?s)?\W',_get_text(doc))
	features['subreddit'] = doc["subreddit"]
	features['apple|ios|mac'] = bareword_match('apple|ios|mac', doc['subreddit'])
	features['apples_to_oranges'] = bareword_match('(A|a)pples (to|and) ((O|o)ranges|apples)', _get_text(doc))
	return features

def apple_pattern():
	return re.compile('(^|\s)(A|a)pple((\')?s)?(\s|$)')

def mac_pattern():
	return re.compile('\W(M|m)ac(intosh)?((\')?s)?\W')

def subreddit_pattern():
	return re.compile('apple|ios|mac')

def apples_to_oranges_pattern():
	return re.compile('(A|a)pples (to|and) ((O|o)ranges|apples)')

def get_apples(is_not_apple=MongoClient("localhost",27017).apple.is_not_apple,is_apple=
	MongoClient("localhost",27017).apple.is_apple):
	is_ 	= [( doc, "is_apple") for doc in is_apple.find()]
	is_not 	= [( doc, "is_not_apple") for doc in is_not_apple.find()]
	return is_ + is_not

def _get_text(doc):
	return doc["body"] if "body" in doc else doc["selftext"]

def bareword_match(exp,comment):
	pattern = re.compile(exp)
	if pattern.search(comment):
		return True
	else:
		return False