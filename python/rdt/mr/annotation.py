import nltk, re, datetime as dt, json
from nltk.probability import FreqDist

_not_word = re.compile('\.|\$')
_word = re.compile("(\W|\(|\)|\$)")
_s_words = nltk.corpus.stopwords.words('english')

def fix_bad_keys(words):
	for w in words:
		w = _not_word.sub("", w)
		if w:
			yield w

def remove_non_words(words):
	for w in words:
		w = _word.sub("", w)
		if w:
			yield w

# contains some temporary fixes :(
def filter_nouns(nouns):

	a = lambda x : x.lower() not in _s_words
	b = lambda x : len(x) > 3
	nouns = filter(lambda x : a(x) and b(x), nouns)
	nouns = list(remove_non_words(nouns))
	if len(nouns) == 1 and nouns[0] == "None":
		return []
	return fix_bad_keys(nouns)

def fix_keys(dct):
	n_dict = {}
	for ky, vl in dct.items():

		n_ky = _not_word.sub("", ky)
		n_ky = _word.sub("", ky)
		n_dict[n_ky] = dct[ky]
	return n_dict

def filter_keys(dct):
	n_dict = {}
	a = lambda x : x.lower() not in _s_words
	b = lambda x : len(x) > 3
	for ky, vl in dct.items():
		if a(ky) and b(ky):
			n_ky = _not_word.sub("", ky)
			n_ky = _word.sub("", ky)
			n_dict[n_ky] = dct[ky]
	return n_dict

def no_none(dct):
	if "None" in dct:
		del(dct["None"])
	return dct

def filter_words(words):
	return filter_nouns(words)

def freq_dist_iter(docs):
	add_zero = lambda x : "0" + x if len(x) == 1 else x
	for doc in docs:
		#try:
			nouns = doc.get("nouns") or []
			nouns = filter_nouns(nouns)
			nouns = FreqDist(nouns)
			r = []
			for d in doc.get("named_entities") or []:
				ent = "_".join([a[0] for a in d])
				r.append(ent)
			r = fix_bad_keys(r)
			ne = FreqDist(r)
			t = dt.datetime.fromtimestamp(int(doc.get("created_utc") or 0))
			anno = {}
			anno["nouns"] = dict(nouns)
			anno["named_entities"] = dict(ne)
			anno["subreddit"] = {doc.get("subreddit") : 1}
			anno["author"] = {doc.get("author"): 1 }
			anno["datetime"] = {str(t.year) + add_zero(str(t.month)) + add_zero(str(t.day)) : 1}
			yield anno
		#except:
		#	pass

def fix_reader(fl):
	with open(fl) as f:
		for line in f:
			line = line.split('\t')
			name, data = line[0], json.loads("".join(line[1:]))
			data["nouns"] = no_none(filter_keys(fix_keys(data["nouns"])))
			data["named_entities"] = no_none(filter_keys(fix_keys(data["named_entities"])))
			yield name, data

def user_reader(fl):
	for name, data in fix_reader(fl):
		data["author"] = name
		yield data

def author_reader(fl):
	return user_reader(fl)

def ner_reader(fl):
	for ne, data in fix_reader(fl):
		data["named_entity"] = ne
		yield data

def sbr_reader(fl):
	for sbr, data in fix_reader(fl):
		data["subreddit"] = sbr
		yield data