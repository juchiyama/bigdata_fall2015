import pymongo, json

# db.combined.find({ body : { $regex : /((A|a)pple\b)|(Mac(intosh)?\b)|(Steve\s?Jobs\b)|(i\-?(phone|mac|book|tunes|pad|os)\b)/i }}).sort({created_utc : 1})
#  d = db.runCommand( {aggregate : "combined", pipeline : [{ $match :{ body : { $regex : "/((A|a)pple\b)|(Mac(intosh)?)|(Steve\s?Jobs)|(i\-?(phone|mac|book|tunes|pad|os))/i" }}}, { $project : { created_utc : 1, name : 1 } }, { $sort : { created_utc : -1 }}] })

# max for matching appple in body
# d = db.runCommand( {aggregate : "combined", pipeline : [{ $match :{ body : { $regex : "/((A|a)pple\b)|(Mac(intosh)?)|(Steve\s?Jobs)|(i\-?(phone|mac|book|tunes|pad|os))/i" }}}, { $project : { created_utc : 1, name : 1 } }, { $sort : { created_utc : -1 }}, {$group : { _id : "1", max_utc : { $max : "$created_utc"} }} ] })

# max with loose comments
# 1407818331
# min comments
# 1404484139

# min utc submissions
# 1404484280

# max utc submission
# 1407821657

def write_apple_match():
	client = pymongo.MongoClient(host="localhost",port=27017)
	combined = client.reddit_stream.combined
	regex = {"$regex" : "\b((A|a)pple)|(Mac(intosh)?)|(Steve\s?Jobs)|(i\-?(phone|mac|book|tunes|pad|os))\b", "$options" : "i"}
	cond_selftext = {"selftext" : regex }
	cond_body = {"body" : regex }
	# c = combined.find({"selftext" : {"$regex" : "\b((A|a)pple)|(Mac(intosh)?)|(Steve\s?Jobs)|(i\-?(phone|mac|book|tunes|pad|os))\b"}}).sort("created_utc",pymongo.ASCENDING)

	cursor = combined.find(cond_selftext)
	cursor.batch_size(1000)
	f = open("concentrated_submissions_apple.json", "w")
	for document in cursor:
		del document["_id"]
		f.write(json.dumps(document) + "\n")
	f.close()

	cursor = combined.find(cond_body)
	cursor.batch_size(1000)
	f = open("concentrated_comments_apple.json", "w")
	for document in cursor:
		del document["_id"]
		f.write(json.dumps(document) + "\n")
	f.close()

def get_created_utc_range():
	high = 0
	low = 0
	with open("concentrated_apple.json","r") as f:
		for ind, document in enumerate(f):
			document = json.loads(document)
			created_utc = document["created_utc"]
			if ind == 0:
				low = created_utc
			if created_utc < low:
				low = created_utc
			if created_utc > high:
				high = created_utc
	print("this is the time range that discusses apple. Some random distribution of documents will make")
	print("model simple")
	print("LOW", low)
	print("HIGH", high)

def insert_maybe_comments_apple(path="concentrated_comments_apple.json"):
	client = pymongo.MongoClient(host="localhost",port=27017)
	maybe_comments = client.reddit_stream_test.maybe_comments
	with open(path,"r") as f:
		buf = []
		for ind, doc in enumerate(f):
			doc = json.loads(doc)
			buf.append(doc)
			if ind + 1 % 1000 == 0:
				maybe_comments.insert(buf)
				buf = []
		if buf:
			maybe_comments.insert(buf)

def how_many_documents_between(low, high):
	client = pymongo.MongoClient(host="localhost",port=27017)
	combined = client.reddit_stream.combined
	condition = {"created_utc" : {"$gte" : low, "$lte" : high}}
	number = combined.find(condition).sort({"created_utc" : 1}).count()
	print("NUMBER OF DOCUMENT SPANNING APPLE DISCUSSION", number)

if __name__ == "__main__":
	print("Use this module from python REPL.\n enter python shell ( $ python ) and then import the module")