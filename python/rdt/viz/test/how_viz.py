import unittest
import rdt.job as job, nltk
from rdt.job import AnnotatedSource
from pylab import *
import matplotlib.pyplot as plt

class HowVizTestCase(unittest.TestCase):

	def setUp(self):
		self.t = self.assertTrue
		self.inst = self.assertIsInstance


	def tearDown(self):	
		pass

	def test_classifier(self):
		figure(figsize=(8,6),dpi=80)
		subplot(1,1,1)

		X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
		C,S = np.cos(X), np.sin(X)
		"""
		plot(X, C, color="blue", linewidth=2.5, linestyle="-")

		plot(X, S, color="green", linewidth=2.5, linestyle="-")

		xmin, xmax = X.min(), X.max()
		ymin, ymax = Y.min(), Y.max()

		dx = (xmax - xmin ) * 0.2
		dy = (ymax - ymin ) * 0.2

		xlim(xmin - dx, xmax + dx)
		# xlim(-4.0,4.0)

		xticks(np.linspace(-4,4,9,endpoint=True))

		ylim(ymin - dy, ymax + dy)
		# ylim(-1.0,1.0)

		yticks(np.linspace(-1,1,5,endpoint=True))

		show()"""

	def test_what(self):
		plt.plot([1,2,3,4],[1,4,9,16], 'ro')
		plt.axis([0,6,0,20])
		plt.show()