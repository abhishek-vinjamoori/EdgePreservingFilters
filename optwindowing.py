import numpy as np
import cv2
import matplotlib.pyplot as plt

width      = 4096
height     = 2160

def displayOptimizedData(videoFile, optimizedFile, smoothVideoFile, debug, videoType, cropped=False):
    
    global width,height
    Kratio = width/height

    framerate  = 30
    cap = cv2.VideoCapture(videoFile)
    willyFile = open(optimizedFile,'r')
    inputData = willyFile.read()
    windowData = inputData.split('\n')
    yCord      = []
    frameCount = 0
    
    out = cv2.VideoWriter(smoothVideoFile, cv2.VideoWriter_fourcc(*'XVID'), framerate, (640,480))

    while True:
        ret, frame = cap.read()
        
        if cv2.waitKey(1) & 0xFF == ord('q') or ret is False or frameCount>=len(windowData):
            break

        frameData = windowData[frameCount].split()
        # print(frameData)
        
        ym = max(0,min(float(frameData[0]),width))
        xm = max(0,min(float(frameData[1]),height))
        sm = max(0,min(float(frameData[2]),height))

        if xm==0 and ym==0 and sm==0:
            frameCount += 1
            continue

        yCord.append(ym)

        x1 = xm - sm
        y1 = ym - Kratio*sm
        x2 = xm + sm
        y2 = ym + Kratio*sm

        x1 = max(0,min(int(round(float(x1))),height-1))
        y1 = max(0,min(int(round(float(y1))),width-1))
        x2 = max(0,min(int(round(float(x2))),height-1))
        y2 = max(0,min(int(round(float(y2))),width-1))

        # print(frameCount, x1, y1, x2, y2)
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
        


    cap.release()
    cv2.destroyAllWindows()
    out.release()
    willyFile.close()
    
    if debug is True:
        plt.figure()
        plt.plot(yCord)
        plt.show()
