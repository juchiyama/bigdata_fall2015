#!/usr/bin/env python
import sys, json, os
if __name__ == "__main__":
	for line in sys.stdin:
		line = line.rstrip('\n')
		name, doc = line.split("\t")
		sys.stdout.write(doc +"\n")
