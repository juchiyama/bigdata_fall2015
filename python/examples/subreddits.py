import pymongo, nltk, pos


combined = pymongo.MongoClient("balthazar", 27017).reddit_stream.combined

subreddits = []

cursor = combined.find({}, {"subreddit" : 1})
cursor.batch_size(1000)
for doc in cursor[:10000]:
	subreddits.append(doc["subreddit"])


fdist = nltk.FreqDist(subreddits)

sbrs = []
for d in fdist.items()[:10]:
	sbrs.append(d[0])
	print d[0],d[1]

docs = []
comment_sub = lambda x : x["body"] if "body" in x else x["selftext"]

#for d in combined.aggregate( [{ "$match" : { "subreddit" : { "$in" : sbrs }}} ] ):
for d in combined.find({"subreddit" : { "$in" : sbrs }}):
	docs.append(pos.preprocess(comment_sub(d)))
	print docs[0]
	break