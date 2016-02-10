# This program finds the 10 most trafficked subreddits and then
# prints the 10 most common nouns, verbs and abjectives of each subreddit
#
# OBS: It takes a while, but it works!

import pymongo, nltk
from collections import defaultdict
from operator import itemgetter

counts = defaultdict(int)
pos = defaultdict(list)

client = pymongo.MongoClient("localhost",27017)
test = client["reddit_stream_test"]["test"]

cursor = test.find( { }, { 'subreddit': 1, 'body': 1, '_id': 0 } )

for doc in cursor:
	counts[doc['subreddit']] += 1

cursor.rewind()

most_common = sorted(counts.items(), key=itemgetter(1), reverse=True)[:10]
most_common = [t for t,c in most_common]

for doc in cursor:
	if (doc['subreddit'] in most_common):
		if ('body' in doc.keys()):
			pos[doc['subreddit']].extend(nltk.pos_tag(nltk.word_tokenize(doc['body'])))

for subreddit in most_common:
	nouns = (word for (word, tag) in pos[subreddit] if tag == 'NN')
	verbs = (word for (word, tag) in pos[subreddit] if tag == 'VB')
	adjec = (word for (word, tag) in pos[subreddit] if tag == 'JJ')
	nouns_fd = nltk.FreqDist(word for word in nouns)
	verbs_fd = nltk.FreqDist(word for word in verbs)
	adjec_fd = nltk.FreqDist(word for word in adjec)
	print('\n========== ' + subreddit + ' ==========')
	print('\nNOUNS:')
	print(nouns_fd.most_common()[:10])
	print('\nVERBS:')
	print(verbs_fd.most_common()[:10])
	print('\nADJECTIVES:')
	print(adjec_fd.most_common()[:10])
	print('\n')