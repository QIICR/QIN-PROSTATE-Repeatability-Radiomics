import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

def show_bland_altman_plot(title, data1, data2, *args, **kwargs):
  data1     = np.asarray(data1)
  data2     = np.asarray(data2)
  n         = data1.shape[0]
  t         = scipy.stats.t.ppf(0.975, n - 1)

  mean      = np.mean([data1, data2], axis=0)
  diff      = data1 - data2                     # Difference between data1 and data2
  md        = np.mean(diff)                     # Mean of the difference
  sd        = np.std(diff, axis=0, ddof = 1)    # Standard deviation of the difference (ddof = 1 for corrected (unbiased) estimator)
  semd      = np.sqrt(np.square(sd) / n)        # Standard error of md
  ciMd      = t * semd                          # Confidence Interval offset for Mean of differences
  rc        = 1.96 * sd                         # repeatability coefficient
  loaUp     = md + rc                           # limit of agreement (LOA) upper bound
  loaLow    = md - rc                           # limit of agreement (LOA) lower bound
  semdLoa   = np.sqrt((3 * np.square(sd)) / n)  # Standard error of LOA
  ciLoa     = t * semdLoa                       # Confidence Interval offset for LOA
  
  plt.figure(figsize=(8,6))
  
  plt.scatter(mean, diff, *args, **kwargs, zorder = 10)
  
  plt.axhline(md,             color='0.3', linestyle='-')
  plt.axhline(md + ciMd,      color='0.5', linestyle='-.')
  plt.axhline(md - ciMd,      color='0.5', linestyle='-.')
  plt.axhspan(md - ciMd, md + ciMd, color='0.99', zorder = 0)
  
  plt.axhline(loaUp,          color='0.3', linestyle='--')
  plt.axhline(loaUp + ciLoa,  color='0.5', linestyle=':')
  plt.axhline(loaUp - ciLoa,  color='0.5', linestyle=':') 
  plt.axhspan(loaUp - ciLoa, loaUp + ciLoa, color='0.99', zorder = 0)
  plt.axhline(loaLow,         color='0.3', linestyle='--')
  plt.axhline(loaLow + ciLoa, color='0.5', linestyle=':')
  plt.axhline(loaLow - ciLoa, color='0.5', linestyle=':') 
  plt.axhspan(loaLow - ciLoa, loaLow + ciLoa, color='0.99', zorder = 0)
  
  plt.title(title)
  plt.show()

