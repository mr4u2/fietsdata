import tcxparser
import unittest

PARSEFILE = 'F:\\fietsfiles\\2015_history.tcx'

class BasicTest(unittest.TestCase):

    def setUp(self):
        self.fiets = tcxparser.TCXparser(PARSEFILE)

    def tearDown(self):
        pass

class Testers(BasicTest):

    def test_Total_Month_old(self):
        month = 6
        total = 969.91
        calculated_total = self.fiets.total_month_old(2015, month)
        self.assertAlmostEqual(total, calculated_total['dist'] / 1000, 2)

    def test_Total_Month(self):
        month = 6
        total = 969.91
        calculated_total = self.fiets.total_month(2015, month)
        self.assertAlmostEqual(total, calculated_total['dist'] / 1000, 2)
