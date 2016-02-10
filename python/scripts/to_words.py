from rdt.data.mongo.source import Source
from rdt.data.mongo.bulkinserter import BulkInserter
if __name__ == "__main__":
	source = Source(host="localhost",port=27017,database="reddit_stream",collection="combined")
	with BulkInserter(source=Source(host="localhost",port=27017,database='reddit_stream_test',collection='load')) as bulk:
		for doc in source.find_clean(batch_size=1000,limit=2000):
			del doc["_id"]
			bulk.insert(doc)