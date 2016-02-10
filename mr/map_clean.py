#!/usr/bin/env python
import sys, json
if __name__ == "__main__":
	sys.path.insert(0, 'rdt.mod')
	import rdt.data.clean.html as html
	for doc in html.json_iter(sys.stdin):
		ents = json.dumps(doc)
		print(doc["name"] + "\t" + 	ents)
