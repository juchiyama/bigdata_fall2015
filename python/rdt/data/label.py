import nltk, re, pymongo.errors, json 
from pymongo.errors import DuplicateKeyError

def apple_finder(utc,candidates,correct,false,label="is this the correct type"):
	counter = 0
	# if utc indicates to skip some docs
	condition  = do_skip(utc)
	# search for docs, sort by created_utc
	for doc in candidates.find(condition).sort("created_utc", 1):
		# count the documents
		counter += 1
		# print important identifying information
		print ("subreddit ", doc['subreddit'])
		print ("link_title", doc['link_title'])
		print ("")
		print (doc['body'])
		print ("")
		print ("created_utc", doc['created_utc'])
		x = input("(" + str(counter) + ")" + label + " (y or n or q): ")
		# check input
		while not is_good_input(x):
			x = input("(y or n or q): ")
		if x == 'q':
			break
		elif x == 'y':
			# do an insert statement, but do exception handling and delete _id
			insert_into(correct,doc)
		elif x == 'n':
			# do an insert statement, but do exception handling and delete _id
			insert_into(false,doc)
		else:
			raise InputHandlingError(x)
		print( "---------------------")

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
	except DuplicateKeyError as e:
		print ("Duplicate Key error!" + e)
		print (json.dumps(document))
	except:
		print ("Something else happened")

class InputHandlingError(Exception):
	def __init__(self, input):
		self.message = "Bad input: " + input
	def __str__(self):
		return repr(self.message)
