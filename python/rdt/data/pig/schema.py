comment_fields = ['approved_by', 'author', 
					'author_flair_css_class', 
					'banned_by', 'body', 
					'body_html', 'controversiality', 
					'created', 'created_utc', 
					'distinguished', 'downs', 
					'edited', 'fullname', 
					'gilded', 'id', 
					'is_root', 'likes', 
					'link_author', 'link_id', 
					'link_title', 'link_url', 
					'name', 'num_reports', 
					'parent_id', 'permalink', 
					'score', 'score_hidden', 
					'submission', 'subreddit', 
					'subreddit_id', 'ups']

submission_fields = ['author', 'created', 
					'created_utc', 'domain', 
					'downs', 'gilded', 
					'id', 'is_self', 
					'likes', 'name', 
					'num_comments', 'num_reports', 
					'over_18', 'permalink', 
					'score', 'selftext', 
					'selftext_html', 'short_link', 
					'subreddit', 'subreddit_id', 
					'title', 'ups', 'url']

def intersection():
	"""['author', 'created', 'created_utc', 'downs', 'gilded', 'id', 'likes', 'name', 
	'num_reports', 'permalink', 'score', 'subreddit', 'subreddit_id', 'ups']

	"""

	return sorted(list(set(comment_fields).intersection(set(submission_fields))))

def type_mapping():
	d = intersection()
	scheme = {}
	for field in d:
		scheme[field] = "chararray"
	ints = ["created","created_utc","downs","likes","num_reports","score","ups"]
	for intt in ints:
		scheme[intt] = "int"
	scheme["text"] = "chararray"
	return scheme

def type_tuples(more=[],less=[]):
	types = type_mapping()
	tups = [(d,types[d]) for d in list(intersection() + ["text"])]
	tups = set(tups)
	for t in more:
		tups.add(t)
	for t in less:
		tups.remove(t)
	tups = sorted(list(tups), key=lambda x : x[0] + x[1])
	return tups

def fields(more=[],less=[]):
	t = type_tuples(more=more,less=less)
	bits = [":".join([d[0],d[1]]) for d in t]
	bits = ", ".join(bits)
	bits = "( " + bits + " )"
	return bits

def arrange_fields(doc):
	d = []
	for a in doc:
		d.append((a,doc[a]))
	return sorted(d,key=lambda x : str(x[0])+str(x[1]))

def fields_line(doc):
	return "\t".join([str(d[0])+":"+str(d[1]) for d in arrange_fields(doc)])

def default(doc):
	mapp = type_mapping()
	ints = intersection_mutate(doc)
	for d in ints:
		if ints[d] is None:
			if mapp[d] == 'chararray':
				ints[d] = ""
			elif mapp[d] == 'int':
				ints[d] = 0
	return ints


def intersection_mutate(doc):
	doc2 = {}
	if "selftext" in doc:
		doc["text"] = doc["selftext_html"]
	else:
		doc["text"] = doc["body_html"]
	for d in intersection():
		doc2[d] = doc[d]
	doc2["text"] = doc["text"]
	return doc2