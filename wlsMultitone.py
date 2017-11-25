#Multi Scale Tone - Farbman et al 2008

from cvxpy import *
import numpy as np
import scipy
import matplotlib.pyplot as plt

def wls(im, debug):
    
    eps = 2.2204e-16
    IN = np.array(im)
    IN = [i+eps for i in IN]
    IN = np.array(IN)
    N  = len(IN)
    L = np.log(IN)
    alpha = 2
    lamb = 1
    # print("L\n",L)
    smallNum = 0.0001

    r = len(IN)
    k = r
    dy = np.diff(L, axis=0)
    # print("DY SHAPE",dy.shape)
    # print("DY before\n",dy)
    print(dy[0])
    for i in range(N-1):
        dy[i] = -lamb/(np.absolute(dy[i])**alpha + smallNum)

    print("DY after\n",dy)
    dy = np.append(dy,0)

    # print("DX before\n",dx)
    # for i in range(N-1):
    #     dx[i] = -lamb/(np.absolute(dx[i])**alpha + smallNum)

    dx = np.zeros(N-1)
    dx = np.append(dx,0)
    # print("DX after\n",dx)


    B = [dx,dy]
    B = np.array(B)
    d = [-r,-1]
    A = scipy.sparse.spdiags(B,d,k,k)

    e = dx
    w = dx
    s = dy
    n = np.lib.pad(dy, (1,0), 'constant', constant_values=(0))
    n = n[0:N]
    print(e.shape,w.shape,s.shape,n.shape)
    res = (e+w+s+n)
    for i in range(N):
        res[i] = 1-res[i]
        
    # print("res\n",res.shape,res)
    A = A + A.T + scipy.sparse.spdiags(res, 0, k, k)
    # OUT,resid,rank,state = np.linalg.lstsq(A,IN)
    # OUT = scipy.sparse.linalg.lsqr(A,IN)
    OUT = np.linalg.inv(A.toarray())
    # print("OUT\n",OUT.shape,OUT,IN.shape)
    final = np.matmul(OUT,IN)
    # print("Final\n",final.shape,final)
    # print("Input\n",x)
    final = np.reshape(final, (r, 1))
    return final

def getData(transformedFile,debug):
    x = []
    y = []
    s = []
    willyFile = open(transformedFile,'r')
    inputData = willyFile.read()
    windowData = inputData.split('\n')

    for i in windowData:
        frameData = i.split()
        if frameData:
            x.append(float(frameData[0]))
            y.append(float(frameData[1]))
            s.append(float(frameData[2]))

    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    willyFile.close()
    return [x,y,s]

def writeToFile(optimizedFile,output):
    outputData = open(optimizedFile,'w')
    N = len(output[0])
    for i in range(N):
       outputData.write(str(output[0][i]) + ' ' + str(output[1][i])+ ' ' +str(output[2][i]))
       outputData.write('\n')

    outputData.close()    



def main():
    debug = False
    transformedFile = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-transformed.txt'
    optimizedFile   = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-optimized-wls.txt'

    # signal = getData(transformedFile, debug)
    signal = [100]*100 + [200]*100
    signal = np.array(signal, dtype='float64')
    signal += 10*np.random.rand(len(signal))
    signal = [signal]
    output = [0]*len(signal)

    for i in range(len(signal)):
        output[i] = wls(signal[i], debug)
    
    #writeToFile(optimizedFile, output)
    
    #Plotting the results
    figNo = 0 
    plt.figure()
    plt.plot(signal[figNo])
    plt.figure(1)
    plt.plot(output[figNo])
    plt.show()

if __name__ == "__main__":
    main()