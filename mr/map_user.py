#!/usr/bin/env python
import sys, json, datetime as dt
from nltk.probability import FreqDist

def json_iter(ind):
	
	for doc in ind:
		doc = doc.rstrip('\n')
		yield json.loads(doc)

if __name__ == "__main__":
	sys.path.insert(0, 'rdt.mod')
	import rdt.mr.annotation as antate
	# hard work is done in rdt mr annotation
	for doc in antate.freq_dist_iter(json_iter(sys.stdin)):
		#try:
			author = list(doc["author"].keys())[0]
			del(doc["author"])
			print(author + "\t" + json.dumps(doc))
		#except:
		#	pass
