from rdt.data.mongo.features import Features
import sys

if __name__ == "__main__":
	subreddit = sys.argv[1]
	fts = Features(host="localhost",port=27017,database="reddit_stream",collection="features")
	bgrams = list(fts.find({"subreddit" : subreddit}))[0]["bigrams"]
	# bgrams = list(filter(lambda x : True if x[0]))
	while 1:
		print(bgrams)
		print("what do you want remove?")
		word1 = input("enter the first word: ")
		word2 = input("enter the second word: ")
		bgrams = list(filter(lambda x : x[0][0] != word1 and x[0][1] != word2, bgrams))
		action = input("(w)rite, (q)uit, (c)ontinue")
		if action == "w":
			fts.upsert({"subreddit" : subreddit}, {"bigrams" : bgrams})
		if action == "q":
			break