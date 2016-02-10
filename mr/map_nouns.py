#!/usr/bin/env python
import sys, json, datetime as dt
from nltk.probability import FreqDist
from nltk.corpus import stopwords

def json_iter(ind):
	
	for doc in ind:
		doc = doc.rstrip('\n')
		yield json.loads(doc)

if __name__ == "__main__":
	sys.path.insert(0, 'rdt.mod')
	import rdt.mr.annotation as antate
	for doc in antate.freq_dist_iter(json_iter(sys.stdin)):
		try:
			for noun, ct in doc["nouns"].items():
				print(noun + "\t" + json.dumps(doc))
		except:
			pass