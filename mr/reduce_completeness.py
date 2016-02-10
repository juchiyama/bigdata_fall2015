#!/usr/bin/env python
import sys, json

def compare(l1, l2):
	for n1, n2 in zip(l1, l2):
		if(n1 != n2):
			return False
	return True

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

def main():
	result_comment = []
	result_submission = []
	last_comment = '0'
	last_submission = '0'

	for line in sys.stdin:
		line = line.rstrip('\n')
		id_, type_ = line.split("\t")

		if(type_ == 'comment'):
			if(last_comment != '0'):
				tmp_result = generate_list_of_missing_ids(last_comment, id_)
				for missing_id in tmp_result:
					result_comment.append(missing_id)

			last_comment = id_

		else:
			if(last_submission != '0'):
				tmp_result = generate_list_of_missing_ids(last_submission, id_)
				for missing_id in tmp_result:
					result_submission.append(missing_id)

			last_submission = id_

	print("{ \"missing_comments\": " + json.dumps(result_comment) + " }\n")
	print("{ \"missing_submissions\": " + json.dumps(result_submission) + " }\n")

	# sys.stdout.write("{ \"missing_comments\": ")
	# sys.stdout.write(result_comment)
	# sys.stdout.write(" }\n")
	# sys.stdout.write("{ \"missing_submissions\": ")
	# sys.stdout.write(result_submission)
	# sys.stdout.write(" }\n")

if __name__ == "__main__": main()
