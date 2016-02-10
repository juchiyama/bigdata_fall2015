#!/usr/bin/env python
import sys,os,json,datetime as dt

if __name__ == "__main__":
	sys.path.insert(0, 'rdt.mod')
	import rdt.nlp.ngrams as ngrams
	import rdt.nlp.annotate as annotate

	add_zero = lambda x : "0" + x if len(x) == 1 else x
	for doc in sys.stdin:
		doc = doc.rstrip('\n')
		d = annotate.clean_json(doc)
		print(d["name"] + "\t" + json.dumps(d))