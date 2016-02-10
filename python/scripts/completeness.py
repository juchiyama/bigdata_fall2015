#!/usr/bin/python3.4
import sys 
import os
sys.path.append(os.path.relpath("../"))
import rdt.data.mongo.source as src
import pymongo, json, sys, getopt


""" Compare two lists.

	:param l1: The first list to be compared
	:type l1: list

	:param l2: The second list to be compared
	:type l2: list

	:returns: True if the lists are equal (same elements and same order)
			  False, otherwise
	"""
def compare(l1, l2):
	for n1, n2 in zip(l1, l2):
		if(n1 != n2):
			return False
	return True


""" Generates a list of all missing ids between the given
	parameters (first, last), excluding both.

	:param first: The id, which the next one is missing
	:type first: str

	:param last: Another id, which the previous one is missing
	:type last: str

	:returns: list[str]
	"""
def generate_list_of_missing_ids(first='0', last='0'):
	id_list = []
	last_list = []
	iter_list = []

	for c in last:
		last_list.append(ord(c))

	for c in first:
		iter_list.append(ord(c))

	while(not(compare(iter_list, last_list))):
		tmp_list = []
		flag_stop = False

		for n in iter_list[::-1]:
			if(flag_stop):
				tmp_list.append(n)
			else:
				if(n == 57):
					tmp_list.append(97)
					flag_stop = True
				elif(n == 122):
					tmp_list.append(48)
				else:
					tmp_list.append(n + 1)
					flag_stop = True

		del iter_list[:]
		iter_list = []

		for n in tmp_list[::-1]:
			iter_list.append(n)

		del tmp_list[:]
		tmp_list = []

		for n in iter_list:
			tmp_list.append(chr(n))

		id_list.append(''.join(tmp_list))

	del id_list[-1]
	return id_list


""" Find all missing ids in a given Collection.

	:param source: A Collection from MongoDB
	:type source: rdt.data.mongo.source.Source (Collection)

	:returns: list[list[str]]
	"""
def find_missing_ids(source=None):
	if(source == None):
		return None

	cursor = source.find( { }, { 'id': 1, '_id': 0 } )

	cursor = cursor.sort('id')

	ids = []
	result = []

	for doc in cursor[:150]:
		ids.append(doc['id'])

	del ids[0:5]

	last = ids[0]

	for s_id in ids:
		flag_1 = False
		for c1, c2 in zip(last, s_id):
			if(flag_1):
				if(c1 != 'z' or c2 != '0'):
					result.append(generate_list_of_missing_ids(last, s_id))
					break
			else:
				diff = abs(ord(c1) - ord(c2))
				if(diff == 1):
					flag_1 = True
				elif(diff > 1 and diff != 40):
					result.append(generate_list_of_missing_ids(last, s_id))
					break
		last = s_id

	return result


""" Main function. This function creates a instance of a
	MondoDB Collection with the given parameters (default
	or command line arguments), call the function
	find_missing_ids(source) and store the result
	in a file.

	:params: Use python3 completeness.py -h to see the
		list of parameters
	:type: str

	:returns: None
	"""
def main(argv):
	server_ = 'localhost'
	port_ = 27017
	database_ = 'reddit_stream_test'
	collection_ = 'test'
	outputfile = 'output.json'

	try:
		opts, args = getopt.getopt(argv,'hs:p:d:c:o:')
	except getopt.GetoptError:
		print('usage: python3 completeness.py [, <opt> <name>]')
		print('Type python3 completeness.py -h for help')
		sys.exit(2)
	if(opts == []):
		print('This program is running with default parameters')
		print('Type python3 completeness.py -h for help')
	for opt, arg in opts:
		if opt == '-h':
			print('usage: python3 completeness.py [, <opt> <name>]')
			print('-h, Help')
			print('-s, Server name')
			print('-p, Port number')
			print('-d, Database name')
			print('-c, Collection name')
			print('-o, Output file')
			sys.exit()
		elif opt in ('-s'):
			server_ = arg
		elif opt in ('-p'):
			port_ = int(arg)
		elif opt in ('-d'):
			database_ = arg
		elif opt in ('-c'):
			collection_ = arg
		elif opt in ('-o'):
			outputfile = arg

	source = src.Source(host=server_, port=port_, database=database_, collection=collection_)

	result = find_missing_ids(source)

	f = open(outputfile, 'w')

	f.write('{')
	f.write('"missing_ids": ' + json.dumps(result))
	f.write('}\n')

if __name__ == '__main__': main(sys.argv[1:])



# 0 = 48
# 9 = 57
# A = 97
# Z = 122

# Z - 0 == 74
# A - 9 == 40