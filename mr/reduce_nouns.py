#!/usr/bin/env python
import sys, json, os

def count_incr(dct,fld,dct2):
	if fld not in dct:
		dct[fld] = {}
	for ky,vl in dct2.items():
		if fld in dct[fld]:
			dct[fld][ky] += vl
		else:
			dct[fld][ky] = vl
	return dct

def count_merge(dct1,dct2,flds):
	for fld in flds:
		dct1 = count_incr(dct1,fld,dct2[fld])
	return dct1

def blank():
	return {
		"author" : {},
		"subreddit" : {},
		"datetime" : {},
		"named_entities" : {}
	}

if __name__ == "__main__":
	temp = blank()
	current_author = author = ""
	schema = ["author","subreddit","datetime","named_entities"]
	for line in sys.stdin:
		try:
			"""readline"""
			line = line.rstrip('\n')
			"""split the lines"""
			author, data = line.split("\t")		
			data = json.loads(data)
			"""if in loop"""
			if current_author == author:
				"""add one or init"""
				temp = count_merge(temp,data,schema)
			else:
				"""new key, so print it out"""
				if author and current_author != "":
					"""print the current ( to be old entity ) entity out"""
					print(current_author + "\t" + json.dumps(temp))
					"""reset data"""
					temp = blank()
				"""add the first row of matching info, the very first instance"""
				temp = count_merge(temp,data,schema)
				current_author = author
		except:
			# reset
			current_author = ""
			temp = blank()

	if current_author == author:
		try:
			print(author+ "\t" + json.dumps(temp))
		except:
			pass
