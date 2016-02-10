#!/usr/bin/env python
import json, sys

if __name__ == "__main__":
	db = "reddit_stream_test"
	coll= "combined"
	if len(sys.argv ) == 3:
		db= sys.argv[1]
		coll = sys.argv[2]

	sys.path.insert(0,'rdt.mod')
	import rdt.data.mongo.source as src
	source = src.Source(host="localhost",port=27017,database=db,collection=coll)
	for doc in source.find():
		del(doc["_id"])
		sys.stdout.write(json.dumps(doc) + "\n")
