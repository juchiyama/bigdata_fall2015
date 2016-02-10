#!/usr/bin/python3.4
import scripts.reposts.reposts_nvb as nvb, random, nltk
import sys, getopt, pymongo, json
from collections import defaultdict
import datetime as dt

def zero(number):
	if len(number) == 1:
		return '0' + number
	else:
		return number

def show_infos(classifier, test_set):
	print("Accuracy",nltk.classify.accuracy(classifier, test_set))
	classifier.show_most_informative_features()

def show_test_errors(classifier, docs, begin):
	errors = []
	for (name, tag) in docs[begin:]:
		guess = classifier.classify(nvb.apply_features(name))
		if guess != tag:
			errors.append( (tag, guess, name) )
	for (tag, guess, name) in errors:
		print('correct=%-8s guess=%-8s' % (tag, guess))

	print(len(errors))

def run_classifier(classifier, collection, skip_=0, limit_=5000):
	cursor = collection.find(skip=skip_, limit=limit_)
	cursor.batch_size(1000)

	result = defaultdict(lambda : defaultdict(dict))

	from_ = 0
	to_ = cursor.count(True)

	print('Classifying ' + str(to_) + ' documents...')
	print()

	for i in range(from_, to_):
		# if(i % int(to_ / 10) == 0):
		# 	print('checkpoint ' + str(int((i - from_) / int(to_ / 10))))
		try:
			doc = cursor[i]
			if('body' in doc.keys()):
				print('Classifying document ' + str(i) + ' with name: ' + doc['name'] + '... ', end='')
				guess = classifier.classify(nvb.apply_features(doc))
				if(guess == 'is_repost'):
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

				print('done')
		except UnicodeDecodeError:
			continue

	print(str(to_) + ' documents classified!')

	return result

def main(argv):
	server_ = 'localhost'
	port_ = 27017
	database_ = 'corpora'
	collection_ = 'reddit'
	outputfile = 'output.json'

	try:
		opts, args = getopt.getopt(argv,'hitrc:o:')
	except getopt.GetoptError:
		print('usage: ./reposts_classifier.py [, <opt> <name>]')
		print('Type ./reposts_classifier.py -h for help')
		sys.exit(2)
	if(opts == []):
		opts.append(('-h', ''))
	for opt, arg in opts:
		if opt == '-h':
			print('usage: ./reposts_classifier.py [, <opt> <name>]')
			print('-h, Help')
			print('-i, Show informative features')
			print('-t, Show test_set errors')
			print('-r, Run classifier on reddit copora')
			print('-c, Change collection name')
			print('-o, Output file')
			sys.exit()
		elif opt in ('-i'):
			option = 'i'
		elif opt in ('-t'):
			option = 't'
		elif opt in ('-r'):
			option = 'r'
		elif opt in ('-c'):
			collection_ = arg
		elif opt in ('-o'):
			outputfile = arg

	client = pymongo.MongoClient(server_, port_)
	collection = client[database_][collection_]

	# random.seed(0)
	docs = nvb.get_reposts()
	random.shuffle(docs)
	featuresets = [(nvb.apply_features(doc), what_is) for (doc,what_is) in docs]
	train_set, test_set = featuresets[0:int(len(featuresets)/2)], featuresets[int(len(featuresets)/2) + 1:]
	classifier = nltk.NaiveBayesClassifier.train(train_set)

	if(option == 'i'):
		show_infos(classifier, test_set)
	elif(option == 't'):
		show_test_errors(classifier, docs, len(train_set))
	elif(option == 'r'):
		result = run_classifier(classifier, collection, 0, 20000)

		f = open(outputfile, 'w')

		f.write(json.dumps(result))

if __name__ == '__main__': main(sys.argv[1:])