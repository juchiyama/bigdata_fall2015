#!/usr/bin/env python
import sys, json, os, re
if __name__ == "__main__":
	for line in sys.stdin:
		line = line.rstrip('\n')
		name, doc = line.split("\t")
		doc = json.loads(doc)
		sys.stdout.write(json.dumps(doc) +"\n")
