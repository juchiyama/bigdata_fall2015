import unittest
import rdt.data.mongo.source as source
import praw

if __name__ == "__main__":
	red = praw.Reddit("epsilonbd/1.0 by epsilon natural language processing", site="https://sites.google.com/site/epsilonbdbot/")
	print(red)
	print(red.login( username="", password="" ))
	submissions = red.get_subreddit('news').get_hot(limit=5)
	print([x["link_title"] for x in submissions])

	"""
	bass == fish
	bass == guitar



	"""
