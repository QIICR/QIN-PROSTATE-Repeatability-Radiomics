import unittest
#import _testContext
import os
import numpy as np

import statsUtils.metrics as sm

class TestMetrics(unittest.TestCase):

  def setUp(self):
    pass
  
  def tearDown(self):
    pass

  def test_twoSimpleDataPairsBadCorrelation(self):
    m = sm.getMetrics([1,2], [2,1])
    self.assertEqual(m["mean"], 1.5)
    self.assertEqual(m["std"], 0.5)
    self.assertEqual(m["meanOfDiff"], 0)
    self.assertEqual(m["stdOfDiff"], 1)
    self.assertEqual(m["rc"], 1.96)
    self.assertEqual(m["rcp"], 1.96/1.5)
    self.assertEqual(m["meanOfAbsDiff"], 1)
    self.assertEqual(m["meanOfAbsDiffPercent"], 1/1.5)
    self.assertEqual(m["stdOfAbsDiff"], 0)
    self.assertEqual(m["stdOfAbsDiffPercent"], 0)
    self.assertEqual(m["icc"], -1)
    self.assertEqual(m["bms"], 0)
    self.assertEqual(m["wms"], 0.25)

  def test_twoSimpleDataPairsGoodCorrelation(self):
    m = sm.getMetrics([1,2], [1,2])
    self.assertEqual(m["mean"], 1.5)
    self.assertEqual(m["std"], 0.5)
    self.assertEqual(m["meanOfDiff"], 0)
    self.assertEqual(m["stdOfDiff"], 0)
    self.assertEqual(m["rc"], 0)
    self.assertEqual(m["rcp"], 0)
    self.assertEqual(m["meanOfAbsDiff"], 0)
    self.assertEqual(m["meanOfAbsDiffPercent"], 0)
    self.assertEqual(m["stdOfAbsDiff"], 0)
    self.assertEqual(m["stdOfAbsDiffPercent"], 0)
    self.assertEqual(m["icc"], 1)
    self.assertEqual(m["bms"], 0.5)
    self.assertEqual(m["wms"], 0)

  def test_divisionsByZero(self):
    m = sm.getMetrics([0,0], [0,0])
    self.assertEqual(m["mean"], 0)
    self.assertEqual(m["std"], 0)
    self.assertEqual(m["meanOfDiff"], 0)
    self.assertEqual(m["stdOfDiff"], 0)
    self.assertEqual(m["rc"], 0)
    self.assertTrue(np.isnan(m["rcp"]))
    self.assertEqual(m["meanOfAbsDiff"], 0)
    self.assertTrue(np.isnan(m["meanOfAbsDiffPercent"]))
    self.assertEqual(m["stdOfAbsDiff"], 0)
    self.assertTrue(np.isnan(m["stdOfAbsDiffPercent"]))
    self.assertTrue(np.isnan(m["icc"]))
    self.assertEqual(m["bms"], 0)
    self.assertEqual(m["wms"], 0)


if __name__ == "__main__":
  unittest.main()


