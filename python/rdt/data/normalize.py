import json

def post(document):
	f_map = {}
	for k in document:
		f_map[k] = [none_to_blank]
	for d in document:
		for f in f_map[d]:
			document[d] = f(document[d])
	return document

def none_to_blank(value):
	return "" if value is None else value

def json_str(document,fields=None,mutate=lambda x : x):
	fields = maybe_with_fields(fields)
	return mutate(fields(post(json.loads(document))))

def json_file(loc,fields=None,mutate=lambda x : x):
	fields = maybe_with_fields(fields)
	with open(loc,"r") as f:
		for line in f:
			yield mutate(fields(json_str(line)))

def json_file_to(loc,out,fields=None,mutate=lambda x : x):
	fields = maybe_with_fields(fields)
	with open(out,"w") as f:
		for clean in json_file(loc):
			f.write(json.dumps(mutate(fields(clean))) + "\n")

def maybe_with_fields(fields=None):
	remove = lambda x : with_fields(x,fields)
	if fields is None:
		remove = lambda x : x
	return remove

def with_fields(doc,fields):
	return {d:doc[d] for d in fields}