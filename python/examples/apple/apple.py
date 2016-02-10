import apple_label as label, re, json
import pymongo
# get it


""" the following MongoDB expression over 2 million documents returns around 2000 documents
"""
# db.combined.find({ body : { $regex : /((A|a)pple\b)|(Mac(intosh)?\b)|(Steve\s?Jobs\b)|(i\-?(phone|mac|book|tunes|pad|os)\b)/i }}).sort({created_utc : 1})



if __name__ == "__main__":
	client = pymongo.MongoClient(host="localhost",port=27017)
	is_apple = client.reddit_stream_test.is_apple
	is_not_apple = client.reddit_stream_test.is_not_apple
	maybe_apple = client.reddit_stream_test.maybe_comments

	print( "")
	print( "START!\n")

	try:
		utc = int(input("Enter a unix time stamp\nx > 0 to skip to time\nx < 1 to start at beginning\nx = "))
		if utc < 1:
			print( "dropping " + repr(is_apple))
			print( "is_apple.find().count(): " + str(is_apple.find().count()))
			print( "dropping " + repr(is_not_apple))
			print("is_apple.find().count(): " + str(is_not_apple.find().count()))
			print("")

		print("Starting at utc " + str(utc))
		print("Hello, determine if they comments relate to Apple Inc!")
		print("---------------------")
		label.apple_finder(utc,maybe_apple, is_apple, is_not_apple)
	except ValueError:
		"Give me an int"
	except:
		"you pooped up"
