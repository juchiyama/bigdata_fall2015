#!/usr/bin/env python
import sys, json, os

if __name__ == "__main__":
	temp = {
		"date" : {},
		"subreddit" : {}
	}
	current_ent = ""
	for line in sys.stdin:
		"""readline"""
		line = line.rstrip('\n')
		"""split the lines"""
		ent, dtime, subreddit = line.split("\t")
		"""if in loop"""
		if current_ent == ent:
			"""add one or init"""
			if dtime in temp["date"]:
				temp["date"][dtime] += 1
			else:
				temp["date"][dtime] = 1
			if subreddit in temp["subreddit"]:
				temp["subreddit"][subreddit] += 1
			else:
				temp["subreddit"][subreddit] = 1
		else:
			"""new key, so print it out"""
			if ent and current_ent != "":
				"""print the current ( to be old entity ) entity out"""
				print(current_ent + "\t" + json.dumps(temp))
				"""reset data"""
				temp = {
					"date" : {},
					"subreddit" : {}
				}
			"""add the first row of matching info, the very first instance"""
			temp["date"][dtime] = 1
			temp["subreddit"][subreddit] = 1
			current_ent = ent

	if current_ent == ent:
		print(ent+ "\t" + json.dumps(temp))
