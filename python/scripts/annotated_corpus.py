import rdt.data.clean.html as clean
import rdt.data.mongo.source as rdtcorp
import rdt.nlp.ngrams as ngrams
import rdt.nlp.pos as pos
from nltk.chunk import ne_chunk
from nltk.chunk.util import tree2conlltags
import rdt.nlp.conll_get as cnll

if __name__ == "__main__":
	source = rdtcorp.Source(conf_key="source_test")
	annotated = rdtcorp.Source(conf_key="annotated_test")
	docs = source.find()
	docs.batch_size(1000)
	tagger = ngrams.make_backoff_tagger()
	buf = []
	for ind, doc in enumerate(clean.doc_iter(docs)):
		del(doc["_id"])
		sentences = pos.tokenize_sents(doc["cleansed_text"])
		tags = pos.tokenize_words(sentences)
		doc["conlltags"] = []
		doc["nouns"] = []
		doc["named_entities"] = []
		for sent in tags:
			tagged_sent = tagger.tag(sent)
			d = ne_chunk(tagged_sent)
			chunks = tree2conlltags(d)
			doc["conlltags"].append(chunks)
			doc["nouns"].extend(cnll.get_nouns(chunks))
			doc["named_entities"].extend(cnll.get_ne(chunks))
		buf.append(doc)
		if ind % 1000:
			annotated.insert(buf)
			buf = []
	if buf:
		annotated.insert(buf)
