import cv2 as cv          ################
                                ###################
                           # '''allways implements model complexty'''
import mediapipe as mp
import time
import math
import Timer




class poseDetector  ():
    def __init__(self,mode=False,model_complexity=1,upBody=False,smooth=True,enable_segmentation=False,detectionCon=0.5,trackCon=0.5):

            self.mode=mode
            self.upBody=upBody
            self.smooth=smooth
            self.detectionCon=detectionCon
            self.trackCon=trackCon
            self.enableSeg=enable_segmentation
            self.model_complexity=model_complexity

            self.mpDraw=mp.solutions.drawing_utils
            self.mpPose=mp.solutions.pose
            self.pose=self.mpPose.Pose( self.mode,self.model_complexity, self.upBody, self.smooth,self.enableSeg,self.detectionCon,self.trackCon)

    def findPose(self,img,draw=True):



         imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
         self.results=self.pose.process(imgRGB)

         if self.results.pose_landmarks :
             if draw:
                    self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
                    '''for id,lm in enumerate(results.pose_landmarks.landmark):
                        h,w,c=img.shape


                        cx,cy=int(lm.x*w),int(lm.y*h)
                        cv.circle(img,(cx,cy),10,(255,255,0),cv.FILLED)

                        print(id,lm)
                    '''
         return img
    def getPosition(self ,img,draw=True ):
        self.lst=[]
        for id, lm in enumerate(self.results.pose_landmarks.landmark):
            h, w, c = img.shape

            cx, cy = int(lm.x * w), int(lm.y * h)
            #cv.circle(img, (cx, cy), 10, (255, 255, 0), cv.FILLED)

            self.lst.append([id,cx,cy])
            if draw:
                cv.circle(img,(cx,cy),5,(255,0,0),cv.FILLED)
        return self.lst
    #use landmarks internaly
    def angleDetection(self,img,p1,p2,p3,draw=True ):
            x1,y1=self.lst[p1][1:]
            x2, y2 = self.lst[p2][1:]
            x3, y3 = self.lst[p3][1:]
            angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
            #print(angle)
            if angle<0:
                angle +=360


            if draw :
                cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv.line(img, (x2, y2), (x3, y3), (0, 255, 0), 2)
                cv.circle(img,(x1,y1),5,(244,0,0),cv.FILLED)
                cv.circle(img, (x2, y2), 5, (244, 0, 0), cv.FILLED)
                cv.circle(img, (x3, y3), 5, (244, 0, 0), cv.FILLED)
                cv.putText(img,str(int(angle)),(x2-30,y2-30),cv.FONT_HERSHEY_PLAIN,2,(0,240,230),4)

            return angle
    def figit (self,img,c,isOUt,draw=True):


        x1, y1 = self.lst[0][1:]
        cv.line(img,  (370, 150),(370, 300), (0, 240, 230),3)
        cv.line(img, (320, 150),(320, 300), (0, 240, 230), 3)
        cv.circle(img, (350, y1), 8, (0, 240, 230), cv.FILLED)



        if   x1 <370 and x1>320:
            isOUt=False

        elif x1 >370 or x1<320:
            if not isOUt:
                c+=1
            isOUt=True

            cv.putText(img,"you are out ", (200, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0,230), 4)



        if draw:
           # cv.putText(img, str(int(x1)), ( 130,  30), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
            # cv.putText(img, str(isOUt), (500, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
            cv.putText(img, str(c), (600, 30), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 230), 4)
        return c,isOUt

def main():
    pTime = 0
    cap = cv.VideoCapture(0)
    detector=poseDetector()

    while True:
        succes,img=cap.read()
        img=detector.findPose(img)
        results=detector.getPosition(img)
        print(results)



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (20, 70), cv.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 2)

        cv.imshow("video", img)

        cv.waitKey(1)




if __name__=="__main__":
    main()