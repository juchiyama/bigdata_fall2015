#!/usr/bin/python3.4
import sys 
import pymongo, json, getopt, nltk
import re
import label_reposts as label

def main(argv):
	server_ = 'localhost'
	port_ = 27017
	database_ = 'corpora'
	collection_ = 'reddit'
	outputfile = 'output.json'

	try:
		opts, args = getopt.getopt(argv,'hs:p:d:c:o:')
	except getopt.GetoptError:
		print('usage: ./reposts.py [, <opt> <name>]')
		print('Type ./reposts.py -h for help')
		sys.exit(2)
	if(opts == []):
		print('This program is running with default parameters')
		print('Type ./reposts.py -h for help')
	for opt, arg in opts:
		if opt == '-h':
			print('usage: ./reposts.py [, <opt> <name>]')
			print('-h, Help')
			print('-s, Server name')
			print('-p, Port number')
			print('-d, Database name')
			print('-c, Collection name')
			print('-o, Output file')
			sys.exit()
		elif opt in ('-s'):
			server_ = arg
		elif opt in ('-p'):
			port_ = int(arg)
		elif opt in ('-d'):
			database_ = arg
		elif opt in ('-c'):
			collection_ = arg
		elif opt in ('-o'):
			outputfile = arg

	client = pymongo.MongoClient(server_, port_)
	collection = client[database_][collection_]
	maybe_repost = client[database_]['maybe_repost']

	regex = {"$regex" : "([Rr]epost)", "$options" : "i"}

	cursor = collection.find({'body': regex}, { 'link_id': 1, 'link_author': 1, 'link_title': 1, 'body': 1, 'is_root': 1,
		'subreddit': 1, 'name': 1, 'selftext': 1, 'parent_id': 1, 'created_utc': 1, 'body_html': 1, '_id': 0 }, limit=1000000 )
	cursor.batch_size(1000)

	from_ = 0
	to_ = cursor.count()
	print(to_)

	for i in range(from_, to_):
		if(i % int(to_ / 10) == 0):
			print('checkpoint ' + str(int((i - from_) / int(to_ / 10))))
		try:
			doc = cursor[i]
			if('body' in doc.keys()):
				label.insert_into(maybe_repost, doc)
		except UnicodeDecodeError:
			continue

if __name__ == '__main__': main(sys.argv[1:])