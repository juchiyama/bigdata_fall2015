# from html.parser import HTMLParser
# from lxml import etree
import lxml, re, json, lxml.html, string
from lxml.html.clean import clean_html, Cleaner


"""2.7 vs 3.4 html unescape"""
try:
	import HTMLParser
	html = HTMLParser.HTMLParser()
except ImportError:
	import html

# compile once
no_nbsp 	= re.compile("&nbsp")
no_nl 		= re.compile("\n")
quote 		= re.compile("\\\'")
ellipsis	= re.compile("\.\.\.")

def skip_iter(docs):
	whichever = lambda x : x["selftext"] if "selftext" in x else x["body"]
	for doc in docs:
		if whichever(doc) == "":
			continue
		yield clean_doc(doc)

def doc_iter(docs):
	for doc in docs:
		yield clean_doc(doc)

# the following function takes a lot of liberties
def strip_html(doc):
	_blank_if_none = lambda x : "" if x is None else x
	_empty_div_if_none = lambda x : "<div></div>" if x is None else x
	_nbsp_del 	= lambda x : re.sub(no_nbsp,"",x)
	_no_nl 		= lambda x : re.sub(no_nl, " ", x)
	_quote_fix 	= lambda x : re.sub(quote, "'", x)
	_no_ellipsis = lambda x : re.sub(ellipsis, ".", x)
	_unescape 	= lambda x : html.unescape(_empty_div_if_none(doc))
	_printable = lambda x : "".join(list(filter(lambda x : x in string.printable, x)))
	return _printable(_no_ellipsis(lxml.html.fromstring(clean_html(_no_nl(_unescape(doc)))).text_content()))

def clean_doc(doc):
	_html = lambda x : x["selftext_html"] if "selftext_html" in x else x["body_html"]
	if "selftext_html" in doc:
		doc["cleansed_text"] = strip_html(_html(doc))
	else:
		doc["cleansed_text"] = strip_html(_html(doc))
	return doc

def clean_json(doc):
	return clean_doc(json.loads(doc))

def json_iter(docs):
	for doc in docs:
		try:
			yield clean_json(doc)
		except:
			print(doc)
			break
