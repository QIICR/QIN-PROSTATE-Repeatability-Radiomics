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
    self.assertEqual(m["iccConfIntLow"], -1.0)
    self.assertEqual(m["iccConfIntUp"], -1.0)
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
    self.assertTrue(np.isnan(m["iccConfIntLow"]))
    self.assertTrue(np.isnan(m["iccConfIntUp"]))
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
    self.assertTrue(np.isnan(m["iccConfIntLow"]))
    self.assertTrue(np.isnan(m["iccConfIntUp"]))
    self.assertEqual(m["bms"], 0)
    self.assertEqual(m["wms"], 0)

  def test_iccConfidenceIntervals(self):
    m = sm.getMetrics([1, 2, 3], [2, 1, 3])
    self.assertAlmostEqual(m["iccConfIntLow"], -0.3595260832744616)
    self.assertAlmostEqual(m["iccConfIntUp"], 0.977074556239113)
  
  def test_larger_datsets(self):
    d1 = [12, 14, 16, 18, 20, 22, 24, 28, 30, 32]
    d2 = [13, 13, 15, 17, 21, 20, 23, 27, 32, 31]
    m = sm.getMetrics(d1, d2)
    print("\nTimepoint 1 datapoints:", d1)
    print("Timepoint 2 datapoints:", d2)
    print("ICC:", m["icc"])
    print("ICC CI [{} , {}]".format(m["iccConfIntLow"], m["iccConfIntUp"]))
    
    d1 = [123, 134, 132, 118, 145, 110, 119, 100, 156, 145]
    d2 = [134, 112, 102, 119, 123, 134, 123, 114, 136, 112]
    m = sm.getMetrics(d1, d2)
    print("\nTimepoint 1 datapoints:", d1)
    print("Timepoint 2 datapoints:", d2)
    print("ICC:", m["icc"])
    print("ICC CI [{} , {}]".format(m["iccConfIntLow"], m["iccConfIntUp"]))

    d1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    d2 = [2, 3, 5, 4, 6, 7, 9, 8, 11, 10]
    m = sm.getMetrics(d1, d2)
    print("\nTimepoint 1 datapoints:", d1)
    print("Timepoint 2 datapoints:", d2)
    print("ICC:", m["icc"])
    print("ICC CI [{} , {}]".format(m["iccConfIntLow"], m["iccConfIntUp"]))




if __name__ == "__main__":
  unittest.main()


