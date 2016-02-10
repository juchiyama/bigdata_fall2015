#!/usr/bin/env python
import sys, json
import datetime as dt
from collections import defaultdict

def zero(number):
	if len(number) == 1:
		return '0' + number
	else:
		return number

def main():
	result = defaultdict(lambda : defaultdict(dict))

	for line in sys.stdin:
		line = line.rstrip('\n')
		tag, doc = line.split("\t")
		doc = json.loads(doc)

		if(tag == 'is_repost'):
			t = dt.datetime.fromtimestamp(int(doc['created_utc']))
			date = str(t.year) + zero(str(t.month)) + zero(str(t.day))

			if(doc['link_author'] in result.keys()):
				if(doc['link_author'][date] in result[doc['link_author']].keys()):
					if(doc['subreddit'] in result[doc['link_author']][date].keys()):
						result[doc['link_author']][date][doc['subreddit']] += 1
					else:
						result[doc['link_author']][date][doc['subreddit']] = 1
				else:
					result[doc['link_author']][date][doc['subreddit']] = 1
			else:
				result[doc['link_author']][date][doc['subreddit']] = 1


	sys.stdout.write(json.dumps(result) +"\n")

if __name__ == "__main__": main()
