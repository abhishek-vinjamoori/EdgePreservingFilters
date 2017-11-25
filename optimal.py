from cvxpy import *
import numpy as np
import scipy
import matplotlib.pyplot as plt

def optimizeData(transformedFile, optimizedFile, parameters, debug):

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
            x.append(frameData[0])
            y.append(frameData[1])
            s.append(frameData[2])

    N = len(x)
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    e = [1]*N
    

    D1 = scipy.sparse.spdiags(np.array([e,[-1*i for i in e]]), np.array([0,1]), N-1,N).toarray()
    D2 = scipy.sparse.spdiags(np.array([e,[-2*i for i in e],e]), np.array([0,1,2]), N-2, N).toarray()
    D3 = scipy.sparse.spdiags(np.array([[-1*i for i in e],[3*i for i in e],[-3*i for i in e],e]), np.array([0,1,2,3]), N-3, N).toarray()



    print(D1,D2,D3)
    print("Shape",D1.shape,D2.shape,D3.shape)
    Xr = Variable(N)
    Yr = Variable(N)
    Sr = Variable(N)

    lambda1 = parameters[0]
    lambda2 = parameters[1]
    lambda3 = parameters[2]

    Objective = Minimize(0.5*sum_squares(x-Xr) +0.5*sum_squares(y-Yr) +0.5*sum_squares(s-Sr) \
        + lambda1*norm(D1*Xr,1) \
        + lambda2*norm(D2*Xr,1) \
        + lambda3*norm(D3*Xr,1) \
        + lambda1*norm(D1*Yr,1) \
        + lambda2*norm(D2*Yr,1) \
        + lambda3*norm(D3*Yr,1) \
        + lambda1*norm(D1*Sr,1) \
        + lambda2*norm(D2*Sr,1) \
        + lambda3*norm(D3*Sr,1))
    prob = Problem(Objective)

    print("Optimal value", prob.solve())
    # print(Sr.value)
    print(Xr.value)
    print("XXXXXXXXXXXX\n",Xr.value.shape)
    for i in range(N):
        outputData.write(str(Xr[i].value) + ' ' + str(Yr[i].value)+ ' ' +str(Sr[i].value))
        if i!=N-1:
            outputData.write('\n')
    
    plt.figure()
    plt.plot(x)
    plt.figure(1)
    plt.plot(Xr.value)
    plt.show()
    willyFile.close()
    outputData.close()



def main():
    debug = False
    videoFile       = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1.mp4'
    dosData         = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy.txt'
    transformedFile = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-transformed.txt'
    optimizedFile   = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-optimized.txt'

    optimizeData(transformedFile,optimizedFile,debug)

if __name__ == "__main__":
    main()