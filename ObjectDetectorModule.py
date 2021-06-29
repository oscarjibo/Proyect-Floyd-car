import cv2
import time


classNames= []
classFile = '/home/pi/Desktop/Object_Detection_Files/coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = '/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = '/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(160,160)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img,thres,nms,draw=True,objetos=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objetos) == 0: objetos=classNames
    objectinfo=[]


    if len(classIds) != 0:

        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            classname = classNames[classId - 1]
            if classname in objetos:
                objectinfo.append([classname])
                if draw:
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classname.upper(),(box[0]+10,box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    return img,objectinfo

if __name__ =="__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    #cap.set(100,80)
    while True:
            success,img = cap.read()
            result,objectinfo = getObjects(img,0.45,0.2,True,objetos=[])
            print(objectinfo)
            cv2.imshow("Output",img)
            cv2.waitKey(1)