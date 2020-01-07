from unittest import TestCase
import os

import grippy

class TestMultiGridWave(TestCase):
	MULTIGRID_GRIB_FILE = os.path.join(os.path.dirname(__file__), 'data', 'multi_1.at_10m.t00z.f005.grib2')

	def test_read(self):
		messages = grippy.message.read_messages(TestMultiGridWave.MULTIGRID_GRIB_FILE)
		self.assertTrue(len(messages) > 0)
