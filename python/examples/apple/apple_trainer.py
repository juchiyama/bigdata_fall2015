import nltk
import re
import pymongo.errors
import json
from pymongo.errors import DuplicateKeyError

def apple_finder(utc,maybe_apple,is_apple,is_not_apple):
	counter = 0
	# if utc indicates to skip some comments
	condition  = do_skip(utc)
	# search for comments, sort by created_utc
	for comment in maybe_apple.find(condition).sort("created_utc", 1):
		# count the documents
		counter += 1
		# print important identifying information
		print ("subreddit ", comment['subreddit'])
		print ("link_title", comment['link_title'])
		print ("")
		print (comment['body'])
		print ("")
		print ("created_utc", comment['created_utc'])
		x = raw_input("(" + str(counter) + ")" + " is this Apple Inc. ? (y or n or q): ")
		# check input
		while not is_good_input(x):
			x = raw_input("(y or n or q): ")
		if x == 'q':
			break
		elif x == 'y':
			# do an insert statement, but do exception handling and delete _id
			insert_into(is_apple,comment)
		elif x == 'n':
			# do an insert statement, but do exception handling and delete _id
			insert_into(is_not_apple,comment)
		else:
			raise InputHandlingError(x)
		print "---------------------"

def do_skip(utc=0):
	if utc < 1:
		return {}
	elif utc >= 1:
		return {'created_utc' : {'$gt' : utc} }

# is it good input?
def is_good_input(x):
	if x == 'q' or x == 'y' or x == 'n':
		return True
	else:
		return False

def insert_into(collection,document):
	try:
		del document['_id']
	except KeyError:
		pass
	try:
		collection.insert(document)
	except DuplicateKeyError, e:
		print ("Duplicate Key error!" + e)
		print json.dumps(document)
	except:
		print ("Something else happened")

class InputHandlingError(Exception):
	def __init__(self, input):
		self.message = "Bad input: " + input
	def __str__(self):
		return repr(self.message)
