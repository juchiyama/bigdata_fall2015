#!/usr/bin/env python
import sys, json

def json_iter(ind):
	for doc in ind:
		doc = doc.rstrip('\n')
		yield json.loads(doc)

def main():
	for doc in json_iter(sys.stdin):
		if(doc['name'].startswith('t1')):
			print(doc['id'] + '\t' + 'comment')
		elif(doc['name'].startswith('t3')):
			print(doc['id'] + '\t' + 'submission')

if __name__ == "__main__": main()
