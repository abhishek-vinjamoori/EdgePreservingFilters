#Bilateral Filtering - Tomasi 1998
# Link - https://users.cs.duke.edu/~tomasi/papers/tomasi/tomasiIccv98.pdf


from cvxpy import *
import numpy as np
import scipy
import matplotlib.pyplot as plt

def gaussmf(var,sigmaV,mean):
    return  np.exp(-(var - mean)**2/(2*(sigmaV**2)))

def bilateralFilter(im, windowSize, sigmaD, sigmaR, debug): 

    N = len(im)
    
    [xGrid, yGrid] = np.mgrid[-windowSize:windowSize+1,-windowSize:windowSize+1]
    xGrid = np.asfarray(xGrid)
    yGrid = np.asfarray(yGrid)
    # print(xGrid,"\n\n\n",yGrid)

    for i in range(xGrid.shape[0]):
        for j in range(xGrid.shape[1]):
            xGrid[i,j] = gaussmf(xGrid[i,j],sigmaD,0)

    for i in range(yGrid.shape[0]):
        for j in range(yGrid.shape[1]):
            yGrid[i,j] = gaussmf(yGrid[i,j],sigmaD,0)

    # print(xGrid,"\n\n\n",yGrid)
    final = np.empty([im.shape[0]])
    distanceGaussian = np.multiply(xGrid,yGrid)
    # print(distanceGaussian)

    for i in range(N):
        iDiff = i - windowSize; 
        iSum  = i + windowSize;
        jDiff = -windowSize; 
        jSum  = windowSize;

        if iDiff >=1:
            startX = iDiff
        else:
            startX = 0

        if iSum >=N:
            endX = N-1
        else:
            endX = iSum
   
        if jDiff>=1:
            startY = jDiff
        else:
            startY = 0
   
        if jSum >=1:
            endY = 0
        else:
            endY = jSum
        # print(startX-iDiff,endX-iDiff +1,startY-jDiff,endY-jDiff +1,startX,endX)
        croppedGaussian   = distanceGaussian[startX-iDiff:endX-iDiff +1,startY-jDiff:endY-jDiff +1]
        # print(croppedGaussian.shape)
        intensityGauss    = im[startX:endX+1];
        # print(intensityGauss.shape)
        intensityGaussian = np.zeros([1,intensityGauss.shape[0]])
        # intensityGaussian = gaussmf(intensityGauss,[sigmaR originalImage(i,j)]);
        for k in range(intensityGaussian.shape[1]):
                intensityGaussian[0,k] = gaussmf(intensityGauss[k],sigmaR,im[i])

        # print(intensityGaussian,"\n\n")
        # print(croppedGaussian,"\n\n\n\n")
        weight = np.multiply(intensityGaussian,croppedGaussian)
        # if np.sum(intensityGaussian) == 0:
            # print(i)
        # print(weight,"\n",intensityGauss,"\n",np.multiply(intensityGauss,weight),"\n\n\n")
        final[i] = np.sum(np.multiply(intensityGauss,weight))/np.sum(weight)

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



def optimizeData(transformedFile, optimizedFile, parameters, debug):
    

    signal = getData(transformedFile,debug)

    output = [0]*len(signal)

    windowSize     = parameters[0]
    sigmaD         = parameters[1]
    sigmaR         = parameters[2]
    
    for i in range(len(signal)):
        output[i] = bilateralFilter(signal[i], windowSize, sigmaD, sigmaR, debug)
    
    writeToFile(optimizedFile, output)
    #Plotting the results
    figNo = 0 
    plt.figure()
    plt.plot(signal[figNo], label='Original Signal')
    plt.figure(1)
    plt.plot(output[figNo], label='Filtered Output')
    plt.legend()
    plt.show()



def main():
    debug = False
    transformedFile = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-transformed.txt'
    optimizedFile   = '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-optimized-bil.txt'

    signal = getData(transformedFile,debug)

    output = [0]*len(signal)

    for i in range(len(signal)):
        output[i] = bilateralFilter(signal[i], windowSize, sigmaD, sigmaR, debug)
    
    # writeToFile(optimizedFile, output)
    #Plotting the results
    figNo = 0 
    plt.figure()
    plt.plot(signal[figNo], label='Original Signal')
    plt.figure(1)
    plt.plot(output[figNo], label='Filtered Output')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()