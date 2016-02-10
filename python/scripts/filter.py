import apple_label as label
from rdt.data.mongo.source import Source

if __name__ == "__main__":
	is_good = Source(host="localhost", port=27017, database='reddit_stream_test',collection='is_good')
	is_bad = Source(host="localhost", port=27017, database='reddit_stream_test', collection='is_bad')

	print( "")
	print( "START!\n")

	try:
		utc = int(input("Enter a unix time stamp\nx > 0 to skip to time\nx < 1 to start at beginning\nx = "))
		if utc < 1:
			print( "dropping " + repr(is_apple))
			print( "is_apple.find().count(): " + str(is_good.count()))
			print( "dropping " + repr(is_not_apple))
			print("is_apple.find().count(): " + str(is_bad.count()))
			print("")

		print("Starting at utc " + str(utc))
		print("Hello, determine if they comments relate to Apple Inc!")
		print("---------------------")
		label.apple_finder(utc,maybe_apple, is_apple, is_not_apple)
	except ValueError:
		"Give me an int"
	except:
		"you pooped up"
