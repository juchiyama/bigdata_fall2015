#!/usr/bin/python3.4
import label_reposts as label, pymongo, sys

def main(argv):
	server_ = 'localhost'
	port_ = 27017
	database_ = 'corpora'
	collection_r = 'reddit'
	collection_ir = 'is_repost'
	collection_inr = 'is_not_repost'

	client = pymongo.MongoClient(host=server_,port=port_)
	reddit = client[database_][collection_r]
	is_repost = client[database_][collection_ir]
	is_not_repost = client[database_][collection_inr]

	quantity = 308

	if(len(argv) > 0):
		quantity = int(argv[1])

	not_noise = []

	cursor_ir = is_repost.find({}, {'name': 1, '_id': 0})
	for doc in cursor_ir:
		not_noise.append(doc['name'])

	cursor_inr = is_not_repost.find({}, {'name': 1, '_id': 0})
	for doc in cursor_inr:
		not_noise.append(doc['name'])

	cursor_r = reddit.find({}, { 'link_id': 1, 'link_author': 1, 'link_title': 1, 'body': 1, 'is_root': 1,
		'subreddit': 1, 'name': 1, 'selftext': 1, 'parent_id': 1, 'created_utc': 1, 'body_html': 1, '_id': 0 }, limit=5000 )

	cursor_r.batch_size(1000)

	inserted = 0
	count = cursor_r.count()

	for i in range(0, count):
		if(inserted >= quantity):
			break

		try:
			doc = cursor_r[i]
			if('body' in doc.keys()):
				if(doc['name'] not in not_noise):
					label.insert_into(is_not_repost, doc)
					inserted += 1
		except UnicodeDecodeError:
			continue

if __name__ == '__main__': main(sys.argv[1:])