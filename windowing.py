import numpy as np
import cv2
import cvxpy
import matplotlib.pyplot as plt



def transformDramaData(frameData, width, height):

    Kratio     = width/height

    y1 = max(0,min(float(frameData[0]),width))
    x1 = max(0,min(float(frameData[1]),height))
    y2 = max(0,min(float(frameData[2]),width))
    x2 = max(0,min(float(frameData[3]),height))

    x1 = x1 - height/90
    x2 = x2 + (x2-x1)/2
    y1 = (y1+y2)/2 - Kratio*(x2-x1)/2
    y2 = y1 + Kratio*(x2-x1)

    return [x1, y1, x2, y2]

def transformDanceData(frameData, width, height):

    Kratio     = width/height
    
    y1           = max(0,min(float(frameData[0]),width))
    x1           = max(0,min(float(frameData[1]),height))
    windowWidth = max(0,min(float(frameData[2]),height))
    windowHeight  = max(0,min(float(frameData[3]),width))

    x2           = x1 + windowHeight
    y2           = y1 + windowWidth
    
    heightDivisionFactor = 40
    widthDivisonFactor   = 3
    x1 = x1 - height/heightDivisionFactor
    x2 = x2 - (x2-x1)/2
    oldy1 = y1
    y1 = (y1+y2)/2 - Kratio*(x2-x1)/widthDivisonFactor
    y2 = (oldy1+y2)/2 + Kratio*(x2-x1)/widthDivisonFactor

    x1 = max(0,min(int(round(float(x1))),height))
    y1 = max(0,min(int(round(float(y1))),width))
    x2 = max(0,min(int(round(float(x2))),height))
    y2 = max(0,min(int(round(float(y2))),width))        

    return [x1, y1, x2, y2]


def PlayAndGetData(videoFile, dosData, modifiedData, out_file, debug, videoType, cropped=False):
    
    framerate  = 30
    cap        = cv2.VideoCapture(videoFile)
    willyFile  = open(dosData,'r')
    inputData  = willyFile.read()
    windowData = inputData.split('\n')
    outputData = open(modifiedData,'w')
    yCord      = []
    frameCount = 0
    out = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc(*'XVID'), framerate, (640,480))

    while True:
        ret, frame = cap.read()
        
        if cv2.waitKey(1) & 0xFF == ord('q') or ret is False or frameCount>=len(windowData):
            break

        frameData = windowData[frameCount].split()
        
        width   = int(cap.get(3))
        height  = int(cap.get(4))

        if videoType is 0:
            x1, y1, x2, y2 = transformDramaData(frameData, width, height)
        else:
            x1, y1, x2, y2 = transformDanceData(frameData, width, height)
        
        if np.abs(x1-x2)==0 or np.abs(y1-y2)==0:
            outputData.write(str(0)+ ' ' +str(0)+ ' ' +str(0))
            outputData.write('\n')
            frameCount += 1
            continue 
        x1 = max(0,min(int(round(float(x1))),height-1))
        y1 = max(0,min(int(round(float(y1))),width-1))
        x2 = max(0,min(int(round(float(x2))),height-1))
        y2 = max(0,min(int(round(float(y2))),width-1))

        # print(x1, x2, y1, y2)

        outputData.write(str((y1+y2)/2)+ ' ' +str((x1+x2)/2)+ ' ' +str((x2-x1)/2))
        outputData.write('\n')
        yCord.append((y1+y2)/2)
        for j in range(3):        
            frame.itemset(((x1+x2)//2,(y1+y2)//2,j),255)

        for i in range(x1,x2):
            for j in range(3):
                frame.itemset((i,y1,j),255)

        for i in range(x1,x2):
            for j in range(3):
                frame.itemset((i,y2,j),255)

        for i in range(y1,y2):
            for j in range(3):
                frame.itemset((x1,i,j),255)

        for i in range(y1,y2):
            for j in range(3):        
                frame.itemset((x2,i,j),255)

        if debug is False:
            crop_img = frame[x1:x2, y1:y2]
            crop_img = cv2.resize(crop_img,(640,480))
            if cropped is True:
                cv2.imshow('frame',crop_img)            
            else:
                frame = cv2.resize(frame,(1920,1080))
                cv2.imshow('frame',frame)
            out.write(crop_img)
        frameCount += 1
        # print(frameCount)

    # print frameCount
    print(yCord)
    willyFile.close()
    outputData.close()
    cap.release()
    out.release()
    if debug is True:
        plt.figure()
        plt.plot(yCord)
        # plt.show()
    else:
        cv2.destroyAllWindows()
    # plt.close()   