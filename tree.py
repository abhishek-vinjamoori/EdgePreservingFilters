import numpy as np
import matplotlib.pyplot as plt

signal = [-100]*100 + [100]*100
sigma = 0.2
sigmaD = 5
sigmaI = 5

n = len(signal)

I = np.array(signal, dtype='float64')
I += 10*np.random.rand(len(I))
biDist = np.empty((n, n))

dDist = np.tile(np.arange(n), (n, 1))
dDist = np.abs(dDist - np.arange(n).reshape((n, 1)))

# tree precompute
treeDist = np.exp(-dDist/sigma)
treeDist /= treeDist.sum(1, keepdims=True)

#bilat precompute
DDist = np.exp(-np.square(dDist)/(2*sigmaD**2))
IDist = np.abs(np.tile(I, (n, 1)) - I.reshape((n, 1)))
IDist = np.exp(-np.square(IDist)/(2*sigmaI**2))
bilatDist = IDist*DDist
bilatDist /= bilatDist.sum(1, keepdims=True)

weight = bilatDist.dot(treeDist)
output = weight.dot(I)

# SHOW@
plt.figure(1)
plt.plot(I)
plt.figure(1)
plt.plot(output)
plt.show()