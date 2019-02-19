from collections import namedtuple
import numpy as np
import scipy.stats


def getMetrics(data1, data2):
  """ Compute statitical metrics for the evaluation of two-timepoint repeated measeruments.

  Args:
    data1: List of feature values for timepoint 1.
    data2: List of feature values for timepoint 2, order must match data1.

  Returns:
    Dictionary of metrics."""
  data1 = np.asarray(data1)
  data2 = np.asarray(data2)
  allData = np.append(data1, data2)
  n = data1.shape[0]
  
  mean = np.mean(allData)
  std = np.std(allData, axis=0, ddof = 0)  # NOT SURE IF THIS SHOULDN'T BE ddof = 1 !!!!????!!?!?
  
  diff = data1 - data2
  meanOfDiff = np.mean(diff)
  stdOfDiff = np.sqrt(np.sum(diff * diff) / n) # here we assume the real mean of the differences to be 0, 
                                               # which is why we don't subtract it!
                                               # We don't use np.std(diff, axis=0, ddof = 0), because this 
                                               # would estimate the mean from the samples which is most 
                                               # likely not 0!
  rc = 1.96 * stdOfDiff
  rcp = np.abs(np.divide(rc, mean))

  meanOfAbsDiff = np.mean(np.abs(diff))
  meanOfAbsDiffPercent = np.abs(np.divide(meanOfAbsDiff, mean))
  stdOfAbsDiff = np.std(np.abs(diff), axis = 0, ddof = 1)
  stdOfAbsDiffPercent = np.abs(np.divide(stdOfAbsDiff, mean))

  iccMetrics = IccMetrics(data1, data2)
  icc = iccMetrics.getIcc()
  iccConfIntLow, iccConfIntUp = iccMetrics.getConfidenceInterval(0.1)
  bms = iccMetrics._getBms()
  wms = iccMetrics._getWms()
  
  pairwiseMean = np.mean([data1, data2], axis=0)
  #diffCoeff = np.mean(np.abs(diff / pairwiseMean))
  
  metrics = {}
  metrics["mean"] = mean
  metrics["std"] = std
  metrics["meanOfDiff"] = meanOfDiff
  metrics["stdOfDiff"] = stdOfDiff
  metrics["rc"] = rc
  metrics["rcp"] = rcp
  metrics["meanOfAbsDiff"] = meanOfAbsDiff
  metrics["meanOfAbsDiffPercent"] = meanOfAbsDiffPercent
  metrics["stdOfAbsDiff"] = stdOfAbsDiff
  metrics["stdOfAbsDiffPercent"] = stdOfAbsDiffPercent
  metrics["icc"] = icc
  metrics["iccConfIntLow"] = iccConfIntLow
  metrics["iccConfIntUp"] = iccConfIntUp
  metrics["bms"] = bms
  metrics["wms"] = wms
  return metrics



class IccMetrics(object):
  """ Compute ICC metrics based on two-timepoint repeated measeruments.
  
      Only computing ICC(1,1) and hence assuming One-Way Random Effects Model

  Args:
    data1: List of feature values for timepoint 1.
    data2: List of feature values for timepoint 2, order must match data1.
  """
  def __init__(self, data1, data2):
    self.data1 = np.asarray(data1)
    self.data2 = np.asarray(data2)

    self.n = self.data1.shape[0]

    self.mean = np.mean([self.data1, self.data2])
    self.pairwiseMean = np.mean([self.data1, self.data2], axis=0)


  def getIcc(self):
    """ 
    Returns:
      ICC(1,1) based on the two-timepoint repeated measeruments.
    """
    BMS = self._getBms()
    WMS = self._getWms()
    ICC = np.divide((BMS - WMS), (BMS + WMS))
    return ICC


  def _getBms(self):
    return np.sum(np.square(self.pairwiseMean - self.mean)) / (self.n - 1)


  def _getWms(self):
    return np.sum(np.square(self.data1 - self.pairwiseMean) + np.square(self.data2 - self.pairwiseMean)) / (2 * self.n)


  def getConfidenceInterval(self, alpha):
      df1 = self.n # df1 = (N - b)(K - 1) with b = 0 for one-way REM and K = 2 in our case (2 "raters" i.e. measurements)
      df2 = self.n - 1
      BMS = self._getBms()
      WMS = self._getWms()
      F0 = BMS/WMS
      FU = F0 * scipy.stats.f.ppf(1 - (alpha / 2), df1, df2)
      FL = F0 * scipy.stats.f.ppf((alpha / 2), df1, df2)
      ciLow = (FL - 1) / (FL + 1) # (FL - 1) / (FL + K - 1)
      ciUp  = (FU - 1) / (FU + 1) # (FU - 1) / (FU + K - 1)
      return ciLow, ciUp
      




# The folowing is (as far as I understand it) a more general implementation
# for different ICCs which work for k > 2. ICC(1,1) wasn't implemeted though
# and I didn't figure out quickly how to compute the missing MSRW in it's
# general form. But I don't want to loose this code, it would be nice
# to finish it one day and check if the general ICC(1,1) gives the same
# result as my version wich is especially tailored to k = 2 based on
# the formulas Mark G. Vangel gave me.
#
# Call this fuction like: icc = getIcc(np.column_stack([data1, data2]))
#
#def getIcc(data, icc_type='icc2'):
#  ''' 
#  Calculate intraclass correlation coefficient
#
#  ICC Formulas are based on:
#  Shrout, P. E., & Fleiss, J. L. (1979). Intraclass correlations: uses in
#  assessing rater reliability. Psychological bulletin, 86(2), 420.
#
#  icc1:  x_ij = mu + beta_j + w_ij
#  icc2/3:  x_ij = mu + alpha_i + beta_j + (ab)_ij + epsilon_ij
#
#  Code modifed from
#  https://github.com/ljchang/nltools/blob/master/nltools/data.py
#
#  '''
#
#  Y = data
#  [n, k] = Y.shape
#
#  # Degrees of Freedom
#  dfc = k - 1
#  dfe = (n - 1) * (k - 1)
#  dfr = n - 1
#
#  # Sum Square Total
#  mean_Y = np.mean(Y)
#  SST = ((Y - mean_Y) ** 2).sum()
#
#  # create the design matrix for the different levels
#  x = np.kron(np.eye(k), np.ones((n, 1)))  # sessions
#  x0 = np.tile(np.eye(n), (k, 1))  # subjects
#  X = np.hstack([x, x0])
#
#  # Sum Square Error
#  predicted_Y = np.dot(np.dot(np.dot(X, np.linalg.pinv(np.dot(X.T, X))),
#                        X.T), Y.flatten('F'))
#  residuals = Y.flatten('F') - predicted_Y
#  SSE = (residuals ** 2).sum()
#
#  MSE = SSE / dfe
#
#  # Sum square column effect - between colums
#  SSC = ((np.mean(Y, 0) - mean_Y) ** 2).sum() * n
#  MSC = SSC / dfc / n
#
#  # Sum Square subject effect - between rows/subjects
#  SSR = SST - SSC - SSE
#  MSR = SSR / dfr
#
#  if icc_type == 'icc1':
#    # ICC(1,1) = (mean square subject - mean square error) /
#    # (mean square subject + (k-1)*mean square error +
#    # k*(mean square columns - mean square error)/n)
#    # ICC = (MSR - MSRW) / (MSR + (k-1) * MSRW)
#    NotImplementedError("This method isn't implemented yet.")
#
#  elif icc_type == 'icc2':
#    # ICC(2,1) = (mean square subject - mean square error) /
#    # (mean square subject + (k-1)*mean square error +
#    # k*(mean square columns - mean square error)/n)
#    ICC = (MSR - MSE) / (MSR + (k-1) * MSE + k * (MSC - MSE) / n)
#
#  elif icc_type == 'icc3':
#    # ICC(3,1) = (mean square subject - mean square error) /
#    # (mean square subject + (k-1)*mean square error)
#    ICC = (MSR - MSE) / (MSR + (k-1) * MSE)
#
#  return ICC

