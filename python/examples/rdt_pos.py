import unittest

import pos as e_r
import json
import pprint

class POSTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = lambda x, y : self.t(isinstance(x,y))
		self.get_text = lambda x : x["body"] if "body" in x else x["selftext"]
	def tearDown(self):
		pass

	def test_mgdb_pipeline_intermediate(self):
		pp = pprint.PrettyPrinter(indent=4)
		limit = 25
		f = open("combined_sample.json", "r")
		g = open("annotated_posts.json", "w")
		count = 0
		for doc in f:
			doc = json.loads(doc)
			sents = e_r.preprocess(self.get_text(doc))
			doc = {"doc" : doc, "sents" : sents}
			g.write(json.dumps(doc) + "\n")
			count += 1
			if count == limit:
				break
			pp.pprint(doc)
			break
		f.close()
		g.close()
		f = open("annotated_posts.json", "r")
		for doc in f:
			doc = json.loads(doc)
			self.assertTrue(type(doc['sents']) is list)
			self.assertTrue(type(doc['doc']) is dict)
			# list of sentences woo
			for s in sents:
				self.assertTrue(type(s) is list)
				converted = e_r.list_to_tuples(s)
				self.assertTrue(type(converted) is list)
				for j in converted:
					self.assertTrue(type(j) is tuple)
				for t in sents:
					self.assertTrue(type(t) is list)
		f.close()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(POSTestCase)
    what = unittest.TextTestRunner(verbosity=2).run(suite)