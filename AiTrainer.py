import cv2 as cv
import numpy as np

import time
from Timer import Timer

t= Timer()
t.start()

import FaceMeshModule
import FaceModule
import HandTrackingModule
import PoseModule as Pose
import FaceMeshModule
#####
pTime=0
#####


cap= cv.VideoCapture(0)
wCam,hCam=680,480
cap.set(3,wCam)
cap.set(4,hCam)

pose=Pose.poseDetector()
hand=HandTrackingModule.handDetector()
face=FaceMeshModule.FaceMesh()
faceD=FaceModule.FaceDetection()
bol =False
count=0
counter=0
isOUt=False
mesh=FaceMeshModule.FaceMesh()

counter1=0
counter=0
bol=True
firstIn=False
stable=False


box=[100,200,100,100]
while True:
    success, img = cap.read()
    img=hand.findHands(img)
    handLand=hand.findPosition(img)
    lx=box[0] + box[2]
    ly=box[1]+box[3]
    x=box[0]
    y=box[1]
    if t.timee() < 40:

        # img, l = face.getMesh(img)
        img = pose.findPose(img)
        # img=hand.findHands(img)
        # img=faceD.findFaces(img)
        landmark = pose.getPosition(img, draw=False)

        if len(landmark) != 0:
            # print(landmark)
            # left arm
            # pose.angleDetection(img, 12, 14, 16)
            # right arm
            angle = pose.angleDetection(img, 11, 13, 15)
            percentage = np.interp(angle, (170, 30), (0, 100))
            cv.putText(img, str(int(t.timee())), (130, 130), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
            counter1, isOUt = pose.figit(img, counter1, isOUt)
            cv.putText(img, "Test 1", (330, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)

            if angle <= 30:
                if not bol:
                    count += 0.5
                    bol = True
            elif angle >= 160:
                if bol:
                    count += 0.5
                    bol = False

    elif t.timee() > 80:
        cv.putText(img, "you Have Blinked: " + str(int(counter)) + " Times", (10, 280), cv.FONT_HERSHEY_PLAIN, 3,
                   (0, 240, 230), 4)
        cv.putText(img, "you Have Figited: " + str(int(counter1)) + " Times", (10, 380), cv.FONT_HERSHEY_PLAIN, 3,
                   (0, 240, 230), 3)
        if counter + counter1 * 2 > 50:
            result = " may bave Autism "
        else:
            result = " dont have Autism "

        cv.putText(img, "you : " + result, (10, 420), cv.FONT_HERSHEY_PLAIN, 3, (0, 240, 230), 3)


    else:
        img, face = mesh.getMesh(img)
        if len(face) != 0:
            f = face[0]
            if len(f) != 0:

                lb = f[23][2]
                lt = f[159][2]
                ll = f[130][1]
                lr = f[243][1]
                blink = int((lb - lt) / (lr - ll) * 100)
                if blink <= 30:
                    if bol:
                        counter += 1
                        bol = False


                else:
                    bol = True

                cv.putText(img, str(counter), (150, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 135, 40), 2)
                cv.putText(img, str(int(t.timee())), (100, 130), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
                cv.putText(img, "Test 2", (330, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)


    #faceD.fancyDraw(img,bbox=box)

    ###


    cTime=time.time()

    fps=1/(cTime-pTime)

    pTime=cTime
    cv.putText(img,str(int(fps)),(40,70),cv.FONT_HERSHEY_PLAIN,3,(0,0,155),2)





    cv.imshow("Trainer",img)

    cv.waitKey(1)
def sympToms():
    if t.timee() < 40:

        # img, l = face.getMesh(img)
        img = pose.findPose(img)
        # img=hand.findHands(img)
        # img=faceD.findFaces(img)
        landmark = pose.getPosition(img, draw=False)

        if len(landmark) != 0:
            # print(landmark)
            # left arm
            # pose.angleDetection(img, 12, 14, 16)
            # right arm
            angle = pose.angleDetection(img, 11, 13, 15)
            percentage = np.interp(angle, (170, 30), (0, 100))
            cv.putText(img, str(int(t.timee())), (130, 130), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
            counter1, isOUt = pose.figit(img, counter1, isOUt)
            cv.putText(img, "Test 1", (330, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)

            if angle <= 30:
                if not bol:
                    count += 0.5
                    bol = True
            elif angle >= 160:
                if bol:
                    count += 0.5
                    bol = False

    elif t.timee() > 80:
        cv.putText(img, "you Have Blinked: " + str(int(counter)) + " Times", (10, 280), cv.FONT_HERSHEY_PLAIN, 3,
                   (0, 240, 230), 4)
        cv.putText(img, "you Have Figited: " + str(int(counter1)) + " Times", (10, 380), cv.FONT_HERSHEY_PLAIN, 3,
                   (0, 240, 230), 3)
        if counter + counter1 * 2 > 50:
            result = " may bave Autism "
        else:
            result = " dont have Autism "

        cv.putText(img, "you : " + result, (10, 420), cv.FONT_HERSHEY_PLAIN, 3, (0, 240, 230), 3)


    else:
        img, face = mesh.getMesh(img)
        if len(face) != 0:
            f = face[0]
            if len(f) != 0:

                lb = f[23][2]
                lt = f[159][2]
                ll = f[130][1]
                lr = f[243][1]
                blink = int((lb - lt) / (lr - ll) * 100)
                if blink <= 30:
                    if bol:
                        counter += 1
                        bol = False


                else:
                    bol = True

                cv.putText(img, str(counter), (150, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 135, 40), 2)
                cv.putText(img, str(int(t.timee())), (100, 130), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
                cv.putText(img, "Test 2", (330, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)

