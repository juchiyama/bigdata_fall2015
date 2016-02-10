import re
from pymongo import MongoClient

def regex_bigram(word1, word2):
	fl1 = ''
	fl2 = ''

	if(word1[0].isalpha()):
		fl1 = word1[0]

	if(word2[0].isalpha()):
		fl2 = word2[0]

	regex = '.*(\s|^)[' + fl1.upper() + fl1.lower() + ']' + word1[1:] + '.*[' + fl2.upper() + fl2.lower() + ']' + word2[1:]

	return regex

def apply_features(doc):
	features = {}
	features['regex(repost)'] = bareword_match('^(([Rr]epost)|(REPOST))((\.*)|(!*))$',_get_text(doc))
	features['regex([repost])'] = bareword_match('(\s|^)(\[repost(ing)?\])(\s|\()',_get_text(doc))
	features['regex(is_repost)'] = bareword_match('((\s|^)([Ii]t )?is( a [a-z]*)? repost((\.)|(!))?)',_get_text(doc))
	features['bigram(repost,repost)'] = bareword_match(regex_bigram('repost','repost'),_get_text(doc))
	features['bigram(artist,reposting)'] = bareword_match(regex_bigram('artist','reposting'),_get_text(doc))
	features['bigram(stop,reposting)'] = bareword_match(regex_bigram('stop','reposting'),_get_text(doc))
	features['bigram(old,repost)'] = bareword_match(regex_bigram('old','repost'),_get_text(doc))
	features['bigram(OP,repost)'] = bareword_match(regex_bigram('OP','repost'),_get_text(doc))
	features['bigram(repost,frontpage)'] = bareword_match(regex_bigram('repost','frontpage'),_get_text(doc))
	# features['regex(artist_reposting)'] = bareword_match('\s(Artist Reposting \*\*\()',_get_text(doc))
	# features['regex(stop_reposting)'] = bareword_match('(\s|^)([Ss]top reposting)', _get_text(doc))

	features['regex(bot)'] = bareword_match('\*\[I am a bot\]',_get_text(doc))
	features['regex(not_repost)'] = bareword_match('((\s|^)([Ii]t )?is not( a [a-z]*)? repost((\.)|(!))?)',_get_text(doc))
	features['regex(should_repost)'] = bareword_match('(\s|^)([Yy]ou should repost)\s',_get_text(doc))
	features['bigram(please,repost)'] = bareword_match(regex_bigram('please','repost'),_get_text(doc))
	features['bigram(problems,reposting)'] = bareword_match(regex_bigram('problems','reposting'),_get_text(doc))
	features['bigram(free,repost)'] = bareword_match(regex_bigram('free','repost'),_get_text(doc))
	# features['regex(free_to_repost)'] = bareword_match('\s(free to repost)',_get_text(doc))
	return features

# def apple_pattern():
# 	return re.compile('(^|\s)(A|a)pple((\')?s)?(\s|$)')

# def mac_pattern():
# 	return re.compile('\W(M|m)ac(intosh)?((\')?s)?\W')

# def subreddit_pattern():
# 	return re.compile('apple|ios|mac')

# def apples_to_oranges_pattern():
# 	return re.compile('(A|a)pples (to|and) ((O|o)ranges|apples)')

def get_reposts(is_not_repost=MongoClient("localhost",27017).corpora.is_not_repost,is_repost=
	MongoClient("localhost",27017).corpora.is_repost):
	is_ 	= [( doc, "is_repost") for doc in is_repost.find()]
	is_not 	= [( doc, "is_not_repost") for doc in is_not_repost.find()]
	return is_ + is_not

def _get_text(doc):
	return doc["body"] if "body" in doc else doc["selftext"]

def bareword_match(exp,comment):
	pattern = re.compile(exp)
	if pattern.search(comment):
		return True
	else:
		return False