#Total Variation - Rudin et al
#Link - http://www.ipol.im/pub/art/2012/g-tvd/article_lr.pdf

from cvxpy import *
import numpy as np
import scipy
import matplotlib.pyplot as plt

def optimizeData(transformedFile, optimizedFile, parameters, debug):
    x = []
    y = []
    s = []
    willyFile = open(transformedFile,'r')
    inputData = willyFile.read()
    outputData = open(optimizedFile,'w')
    windowData = inputData.split('\n')

    for i in windowData:
        frameData = i.split()
        if frameData:
            x.append(frameData[0])
            y.append(frameData[1])
            s.append(frameData[2])

    N = len(x)
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    e = [1]*N

    D1 = scipy.sparse.spdiags(np.array([e,[-1*i for i in e]]), np.array([0,1]), N-1,N).toarray()



    #print(D1)
    #print("Shape",D1.shape)
    Xr = Variable(N)
    Yr = Variable(N)
    Sr = Variable(N)

    lambda1 = parameters[0]

    Objective = Minimize(0.5*sum_squares(x-Xr) + 0.5*sum_squares(y-Yr) + 0.5*sum_squares(s-Sr) \
        + lambda1*norm(D1*Xr,1) \
        + lambda1*norm(D1*Yr,1) \
        + lambda1*norm(D1*Sr,1))
    
    prob = Problem(Objective)

    print("Optimal value", prob.solve())
    # print(Sr.value)
    #print(Xr.value)
    for i in range(N):
       outputData.write(str(Xr[i].value) + ' ' + str(Yr[i].value)+ ' ' +str(Sr[i].value))
       outputData.write('\n')
    #Plotting the results
    plt.figure()
    plt.plot(x)
    plt.figure(1)
    plt.plot(Xr.value)
    plt.show()
    willyFile.close()
    outputData.close()


def main():
    debug = False
    transformedFile = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-transformed.txt'
    optimizedFile   = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-optimized-tv.txt'
    lambda1 = 800
    optimizeData(transformedFile, optimizedFile, lambda1, debug)

if __name__ == "__main__":
    main()
