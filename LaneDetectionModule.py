import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import utlis
from ObjectDetectorModule import *
curveList = []
avgVal=100
# configuracion de las salidas a la arduino
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT) # si va a la derecha
GPIO.setup(13, GPIO.OUT)# si va  ala izquierda
GPIO.setup(15,GPIO.OUT)# si se mantiene recto
def getLaneCurve(img,display=2):

    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = utlis.thresholding(img)

    #### STEP 2
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utlis.drawPoints(imgCopy,points)

    #### STEP 3
    middlePoint,imgHist = utlis.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    #### STEP 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)

    #### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1

    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    intialTrackBarVals = [186, 81, 133, 203 ]
    utlis.initializeTrackbars(intialTrackBarVals)
    frameCounter = 0
    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        curve = getLaneCurve(img,display=2)
        print(curve*100)
        if curve > 14:# giramos derecha
            GPIO.output(11,True)
        else:
            GPIO.output(11,False)

        if curve >=-14:# giramos derecha
            GPIO.output(13,True)
        else:
            GPIO.output(13,False)

        if -14>curve<14:#vamos recto
            GPIO.output(15,True)
        else:
            GPIO.output(15,False)


        #cv2.imshow('Vid',img)
        cv2.waitKey(1)
        success, img = cap.read()
        result, objectinfo = getObjects(img, 0.45, 0.2, True, objetos=['car','person','stop sign'])
        detenerse=0
        persona=0
        carro=0

        for i in objectinfo:

            if i ==['stop sign']:
                print("stop")
                detenerse=1
            elif i ==['stop sign'] :
                detenerse=0
            elif i ==['person']:
                persona=1
            elif i ==['person']:
                persona=0
            elif i ==['car']:
                carro=1
            elif ['car']:
                carro=0

        if carro==1:
            print("carro detectado")
            GPIO.output(5,True)
        else:
                GPIO.output(5,False)

        if detenerse==1:
            GPIO.output(7,True)
            print("señal de stop detectada")
        else:
            GPIO.output(7,False)


        if persona==1:
            print("persona detectada")
            GPIO.output(3,True)
        else :
            GPIO.output(3,False)


        cv2.imshow("Output", img)
        cv2.waitKey(1)

        time.sleep(2)