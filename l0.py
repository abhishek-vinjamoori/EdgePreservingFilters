# L0 norm - Xu et al
# Link- https://sites.fas.harvard.edu/~cs278/papers/l0.pdf

import numpy as np
from scipy.fftpack import fft, ifft, fft2, ifft2, fftshift, ifftshift
import matplotlib.pyplot as plt


def circulantshift(xs, h):
    return np.hstack([xs[h:], xs[:h]] if h > 0 else [xs[h:], xs[:h]])

def circulant_dx(xs, h):
    return (circulantshift(xs, h) - xs)

def psf2otf(psf, N):
    pad = np.zeros((N,))
    n = len(psf)
    pad[:n] = psf
    pad = np.concatenate([pad[n//2:], pad[:n//2]])
    # print(pad)
    otf = fft(pad)
    return otf

def l0_gradient_minimization_1d(I, lmd, beta, beta_max, beta_rate=2.0, max_iter=20):
    S = np.array(I).ravel()
    # prepare FFT
    F_I = fft(S)
    # print(F_I)
    F_denom = np.abs(psf2otf([-1, 1], S.shape[0]))**2.0
    # print(F_denom)
    # optimization
    hp = np.zeros_like(S)
    for i in range(max_iter):
        # with S, solve for hp in Eq. (12)
        hp = circulant_dx(S, 1)
        mask = hp**2.0 < lmd/beta
        hp[mask] = 0.0
        # with hp, solve for S in Eq. (8)
        S = np.real(ifft((F_I + beta*fft(circulant_dx(hp, -1))) / (1.0 + beta*F_denom)))
        # iteration step
        beta *= beta_rate
        if beta > beta_max: 
            break
    # print(i)
    return S

def getData(transformedFile, debug):
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
            if len(frameData)>1:
                y.append(float(frameData[1]))
                s.append(float(frameData[2]))

    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    willyFile.close()
    if y.shape[0] == 0:
        return [x]
    else:
        return [x,y,s]

def writeToFile(optimizedFile,output):
    outputData = open(optimizedFile,'w')
    N = len(output[0])
    for i in range(N):
       outputData.write(str(output[0][i]) + ' ' + str(output[1][i])+ ' ' +str(output[2][i]))
       if i!=N-1:
            outputData.write('\n')
    # for i in range(N):
    #     outputData.write(str(output[0][i]))
    #     if i!=N-1:
    #         outputData.write('\n')
    outputData.close()    


def optimizeData(transformedFile, optimizedFile, parameters, debug):
    
    signal          = getData(transformedFile, debug)
    # print(signal)

    output = [0]*len(signal)

    lmd = parameters[0]
    beta_max = parameters[1]
    beta_rate = parameters[2]
    beta = lmd*0.01
    
    for i in range(len(signal)):
        output[i] = l0_gradient_minimization_1d(signal[i], lmd, beta, beta_max, beta_rate)
    print(output)
    writeToFile(optimizedFile, output)

    #Plotting the results
    figNo = 0 
    plt.figure()
    plt.plot(signal[figNo])
    plt.figure(1)
    plt.plot(output[figNo])
    plt.show()    


def main():
    debug = False
    transformedFile = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-transformed.txt'
    optimizedFile   = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-optimized-l0.txt'
    
    for iter in range(0,10):
        transformedFile = '/home/abhishek/Desktop/Main/Others/BTP/Smoothening/GeneratedData/data' + str(iter) + '.txt'
        optimizedFile   = '/home/abhishek/Desktop/Main/Others/BTP/Smoothening/Generated_l0_Data/data-l0-'+ str(iter) + '.txt'

        signal          = getData(transformedFile, debug)

        output = [0]*len(signal)

        lmd = 1e3
        beta = lmd*0.001
        beta_max = 1e5
        beta_rate = 2.0

        for i in range(len(signal)):
            output[i] = l0_gradient_minimization_1d(signal[i], lmd, beta, beta_max, beta_rate)
        
        writeToFile(optimizedFile, output)

        #Plotting the results
        figNo = 0 
        plt.figure()
        plt.plot(signal[figNo])
        plt.figure(1)
        plt.plot(output[figNo])
        plt.show()

if __name__ == "__main__":
    main()
