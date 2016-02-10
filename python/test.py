import sys, unittest
import rdt.data.clean.test.html as clean_html
import rdt.nlp.test.pos_iter as pos, rdt.nlp.test.chunk as chunk
import rdt.nlp.test.ngrams as bgram
import rdt.nlp.test.backoff as backoff, rdt.nlp.test.ne_chunk as ne_chunk
import rdt.nlp.test.conll_get as conll, rdt.nlp.test.annotate as annotate
import rdt.data.test.normalize as normalize, rdt.nlp.test.classifier as classifier
import rdt.data.mongo.test.cleansource as cleansource
import rdt.nlp.corpus.test.annotate as annotatecls, rdt.test.job as job
import rdt.test.autoclassifier as autoclass
import rdt.data.mongo.test.features as features
from rdt.nlp.test.sbrnb import SubredditClassifierTestCase
from rdt.viz.test.how_viz import HowVizTestCase

if __name__ == '__main__':
	choice = sys.argv[1]
	suite = lambda x : unittest.TestLoader().loadTestsFromTestCase(x)
	runner = lambda x : unittest.TextTestRunner(verbosity=2).run(x)
	run = lambda x : runner(suite(x))
	tests = {
		"clean_html" 	: clean_html.CleanHTMLTestCase,
		"pos_iter"		: pos.CleanHTMLTestCase,
		"ugram_iter"	: chunk.UnigramTestCase,
		"bigram_test"	: bgram.BigramsTestCase,
		"backoff_test"	: backoff.BackOffTestCase,
		"ne_chunk"		: ne_chunk.NEChunkTestCase,
		"conll_get"		: conll.ConllGetTestCase,
		"annotate_iter"	: annotate.AnnotateTestCase,
		"normalize"		: normalize.NormalizeTestCase,
		"classifier"    : classifier.ClassifierTestCase,
		"cleansource"	: cleansource.CleanSourceTestCase,
		"annotatecls"	: annotatecls.PNBAnnotateTestCase,
		"make_words"	: job.AnnotatedSourceTestCase,
		"autoclass"		: autoclass.AutoClassifierTestCase,
		"features"		: features.FeaturesDBTestCase,
		"sbr_classifier": SubredditClassifierTestCase,
		"how_viz"		: HowVizTestCase
	}
	if choice in tests:
		run(tests[choice])
	else:
		print("I need a valid choice. $ python3.4 test.py \"option\"")
