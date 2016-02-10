from textblob import TextBlob
import json, pymongo, nltk
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.classify import PositiveNaiveBayesClassifier
import re

client = pymongo.MongoClient("localhost",27017)
test = client["reddit_stream_test"]["test"]

#successfully tested with a small sample of this collection

cursor = test.find( { }, { 'created':1, 'subreddit_id':1, 'author':1, 'subreddit': 1, 'body': 1, '_id': 0 } )

#this creates three files named below

outputfilematches = 'testoutputmatches.json'
outputfilenomatches = 'testoutputnomatches.json'
finaloutput = 'testoutput.json'

matchingfile = []
nomatchingfile = []	
search_words = set(["russia", "UkraininanConflict", "worldnews", "fucking", "glorious", "cave"])	
# we can pick search words depending on our purpose 

def matching_sentences():

	
	matches = []
	no_matches = []

	"""for some documents"""
	for doc in cursor:
		"""get the body section which may or may not exist"""
		body = sent_tokenize(doc['body'])
		"""get the sentences in the body
		The following for loop needs to change. I'll show an example soon. There is another way to orient fields that is really awesome
		"""
		for sent in body:
			blob = TextBlob(sent)
			for  sentence in blob.sentences:
				words = set(sentence.words)
				"""blob it? get the words the condition needs to hold that a word matches
				the following lines get replaced with their subreddit membership
				"""
				if search_words & words:
					matches.append(str(sentence))
					matchingfile.append(doc)
				else:
					no_matches.append(str(sentence))
					nomatchingfile.append(doc)
	return (matches, no_matches)

matches , nomatches = matching_sentences()
	
	

def getfile():
	matchingfile = []
	nomatchingfile = []	
	cursor.rewind()
	for doc in cursor:
		body = sent_tokenize(doc['body'])
		for sent in body:
			blob = TextBlob(sent)
			for  sentence in blob.sentences:
				words = set(sentence.words)
				if search_words & words:
					matchingfile.append(doc)
					
				else:
					nomatchingfile.append(doc)
					
					
					
	f = open(outputfilematches, 'w')
	f.write('{')
	f.write(json.dumps(matchingfile))
	f.write('}')
	f.write('\n')
	f.close()
	
	g = open(outputfilenomatches, 'w')
	g.write('{')
	g.write(json.dumps(nomatchingfile))
	g.write('}')
	g.write('\n')
	g.close()
	
	

def features(sentence):
	words = sentence.lower().split()
	return dict(('contains(%s)' % w, True) for w in words)

def commonfeatures(sentence):
	words = re.findall(r'\w+',sentence)
	check = set(words)
	if search_words & check:
		return dict(('contains(%s)' % w, True) for w in (search_words & check))
	

def main():
	positive_featuresets = list(map(features, matches))
	unlabeled_featuresets = list(map(features, nomatches))
	classifier = PositiveNaiveBayesClassifier.train(positive_featuresets, unlabeled_featuresets)
	cursor.rewind()
	events = []
	for doc in cursor:
		body = sent_tokenize(doc['body'])
		for sent in body:
			blob = TextBlob(sent)
			if (classifier.classify(features(blob))) is True:
				# to print what is written in the finalout file
				#print ( '"subreddit_id":' + json.dumps(doc['subreddit_id']) + ',"features":' + json.dumps(commonfeatures(str(blob))))
				events.append('{ "subreddit_id":' + json.dumps(doc['subreddit_id']) + ',"features":' + json.dumps(commonfeatures(str(blob))) + '}')
				
				
	f = open(finaloutput, 'w')
	f.write('{')
	f.write(json.dumps(events))
	f.write('}')
	f.write('\n')
	f.close()					
				
				
				
				
if __name__ == '__main__':
	main()
















	