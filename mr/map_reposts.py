#!/usr/bin/env python
import sys, json, random, nltk

def json_iter(ind):
	for doc in ind:
		doc = doc.rstrip('\n')
		yield json.loads(doc)

def main():
	sys.path.insert(0,'reposts.mod')
	import reposts.reposts_nvb as nvb
	docs = nvb.get_reposts()
	random.shuffle(docs)
	featuresets = [(nvb.apply_features(doc), what_is) for (doc,what_is) in docs]
	train_set, test_set = featuresets[0:int(len(featuresets)/2)], featuresets[int(len(featuresets)/2) + 1:]
	classifier = nltk.NaiveBayesClassifier.train(train_set)

	for doc in json_iter(sys.stdin):
		if('body' in doc.keys()):
			guess = classifier.classify(nvb.apply_features(doc))
			print(guess + '\t' + json.dumps(doc))

if __name__ == "__main__": main()
