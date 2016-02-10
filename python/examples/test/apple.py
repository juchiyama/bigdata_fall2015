import unittest, examples.rdt

class AppleTestCase(unittest.TestCase):

	def setUp(self):
		
		self.t = self.assertTrue
	def tearDown(self):
		pass

	def test_trivial(self):
		data = {}

if __name__ == '__main__':
	other = unittest.TestLoader().loadTestsFromTestCase(RedditAPITestCase)
	derg = unittest.TextTestRunner(verbosity=2).run(other)