# Tree Filtering - Bao et al.
# Link - https://pdfs.semanticscholar.org/70aa/65ab542d5eae6b7c997600910974e214eacb.pdf

from cvxpy import *
import numpy as np
import scipy
import matplotlib.pyplot as plt

def optimizeData(transformedFile,optimizedFile,debug):
    x = []
    y = []
    s = []
    willyFile = open(transformedFile,'r')
    outputData = open(optimizedFile,'w')
    inputData = willyFile.read()
    windowData = inputData.split('\n')

    for i in windowData:
        frameData = i.split()
        if frameData:
            x.append(float(frameData[0]))
            y.append(float(frameData[1]))
            s.append(float(frameData[2]))

    N = len(x)
    x = np.asarray(x)
    # y = np.asarray(y)
    # s = np.asarray(s)
    # for i in range(N):
    #     outputData.write(str(Xr[i].value) + ' ' + str(Yr[i].value)+ ' ' +str(Sr[i].value))
    #     outputData.write('\n')
    willyFile.close()
    # outputData.close()

    I = x
    
    sigmaS         = 50
    sigmaR         = 30
    sigma          = 0.2

    biDist = np.empty((N, N))

    dDist = np.tile(np.arange(N), (N, 1))
    dDist = np.abs(dDist - np.arange(N).reshape((N, 1)))

    # tree precompute
    treeDist = np.exp(-dDist/sigma)
    treeDist /= treeDist.sum(1, keepdims=True)

    #bilat precompute
    DDist = np.exp(-np.square(dDist)/(2*sigmaS**2))
    IDist = np.abs(np.tile(I, (N, 1)) - I.reshape((N, 1)))
    IDist = np.exp(-np.square(IDist)/(2*sigmaR**2))
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



def main():
    debug = False
    transformedFile = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-transformed.txt'
    optimizedFile   = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-optimized.txt'

    optimizeData(transformedFile,optimizedFile,debug)

if __name__ == "__main__":
    main()