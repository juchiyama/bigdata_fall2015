#!/usr/bin/python3.4
import json, pymongo
from pymongo.errors import DuplicateKeyError

def repost_finder(utc, maybe_repost, is_repost, is_not_repost):
	counter = 0
	# if utc indicates to skip some comments
	condition  = do_skip(utc)
	# search for comments, sort by created_utc
	# print('here')
	# print(type(maybe_repost))
	cursor = maybe_repost.find(condition).sort('created_utc', pymongo.ASCENDING)
	for comment in cursor:
		# count the documents
		counter += 1
		# print important identifying information
		print_info(comment)
		x = input("(" + str(counter) + ")" + " is this repost? (y or n or m or q): ")
		# check input
		continue_ = check_input(x, maybe_repost, is_repost, is_not_repost, comment, comment['created_utc'])
		print( "---------------------")
		if(not continue_):
			break

def check_input(x, maybe_repost, is_repost, is_not_repost, comment, utc):
	while not is_good_input(x):
		x = input("(y or n or m or q): ")
	if x == 'q':
		return False
	elif x == 'y':
		# do an insert statement, but do exception handling and delete _id
		insert_into(is_repost, comment)
	elif x == 'n':
		insert_into(is_not_repost, comment)
	elif x == 'm':
		name = comment['name']
		cond = {'parent_id': name, 'created_utc': {'$gt' : utc}}
		more = maybe_repost.find(cond).sort('created_utc"', pymongo.ASCENDING)
		if(more.count() != 0):
			print_info(more[0])
			x = input("(" + str(counter) + ")" + " is the first comment a repost? (y or n or m or q): ")
			continue_ = check_input(x, maybe_repost, is_repost, is_not_repost, comment, more[0]['created_utc'])
		else:
			print("There are no more comments below this one.")
			print("---")
			y = input("Is the first comment a repost? (y or n or m or q): ")
			continue_ = check_input(y, maybe_repost, is_repost, is_not_repost, comment, comment['created_utc'])
	else:
		raise InputHandlingError(x)
	return True

def do_skip(utc=0):
	if utc < 1:
		return {}
	elif utc >= 1:
		return {'created_utc' : {'$gt' : utc} }

# is it good input?
def is_good_input(x):
	if x == 'q' or x == 'y' or x == 'n' or x == 'm':
		return True
	else:
		return False

def insert_into(collection, document):
	try:
		del document['_id']
	except KeyError:
		pass
	try:
		collection.insert(document)
	except DuplicateKeyError as e:
		print ("Duplicate Key error!" + e)
		print (json.dumps(document))
	except:
		print ("Something else happened")

def print_info(doc):
	if('body' in doc.keys()):
		print ("subreddit ", doc['subreddit'])
		print ("link_id ", doc['link_id'])
		print ("link_author ", doc['link_author'])
		# print ("author ", doc['author'])
		print ("")
		print (doc['body'])
		print ("")
		print ("is_root ", doc['is_root'])
		print ("name ", doc['name'])
		print ("parent_id ", doc['parent_id'])
		print ("created_utc", doc['created_utc'])
	else:
		print ("subreddit ", doc['subreddit'])
		print ("title ", doc['title'])
		print ("author ", doc['author'])
		print ("")
		if(doc['selftext'] != ''):
			print (doc['selftext'])
		else:
			print (doc['url'])
		print ("")
		print ("created_utc", doc['created_utc'])

class InputHandlingError(Exception):
	def __init__(self, input):
		self.message = "Bad input: " + input
	def __str__(self):
		return repr(self.message)
