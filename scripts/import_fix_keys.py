import sys, json
import rdt.mr.annotation as att

def json_iter(docs):
	for doc in stdin:
		yield json.loads(doc)

def main(args):

	for doc in json_iter():



if __name__ == "__main__": main(sys.argv[1:])