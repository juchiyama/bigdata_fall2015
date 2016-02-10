#!/usr/bin/python3.4
import label_reposts as label
import pymongo
# get it

if __name__ == "__main__":
	server_ = 'localhost'
	port_ = 27017
	database_ = 'corpora'
	collection_mr = 'maybe_repost3'
	collection_ir = 'is_repost3'
	collection_inr = 'is_not_repost3'

	client = pymongo.MongoClient(host=server_,port=port_)
	maybe_repost = client[database_][collection_mr]
	is_repost = client[database_][collection_ir]
	is_not_repost = client[database_][collection_inr]

	print( "")
	print( "START!\n")

	try:
		utc = int(input("Enter a unix time stamp\nx > 0 to skip to time\nx < 1 to start at beginning\nx = "))
		if utc < 1:
			print( "dropping " + repr(is_repost))
			print( "is_repost.find().count(): " + str(is_repost.find().count()))
			print("")
			is_repost.drop()
			print( "dropping " + repr(is_not_repost))
			print( "is_not_repost.find().count(): " + str(is_not_repost.find().count()))
			print("")
			is_not_repost.drop()

		print("Starting at utc " + str(utc))
		print("Hello, determine if they comments relate to reposts")
		print("---------------------")
		label.repost_finder(utc, maybe_repost, is_repost, is_not_repost)
	except ValueError:
		"Give me an int"
	except:
		"you pooped up"
