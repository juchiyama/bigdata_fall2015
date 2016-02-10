import rdt.mr.annotation as annotation
from rdt.data.mongo.bulkinserter import BulkInserter
from rdt.data.mongo.source import Source
import sys

def main(argv):
	inserter = BulkInserter(source=Source(host="localhost",port=27017,database=argv[1],collection=argv[2]))
	for doc in annotation.sbr_reader(argv[0]):
		inserter.insert(item=doc)
	inserter.send()


if __name__ == "__main__": main(sys.argv[1:])
