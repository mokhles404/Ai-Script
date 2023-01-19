
import cv2
import mediapipe as mp
import time
from Timer import Timer
import FaceModule
from random import  randint
class handDetector():
    def __init__(self, mode=False, maxHands=2,modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.modelComplexity=modelComplexity
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                #print(lm.x,lm.y)
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return self.lmList
    def fingersUp(self,img,draw=True):
        self.tips=[4,8,12,16,20]
        fingers = [0]

        landmark=self.lmList

        for id in range(1, 5):

            if landmark[self.tips[id]][2] < landmark[self.tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if fingers[1]==fingers[2]==1:
            return  1
        elif fingers[1] == 1:
            return 2
        else:
            return 0




def main():
    t=Timer()
    t.start()

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    drawRec=FaceModule.FaceDetection

    firstIn = False


    bbox = [50, 100, 200, 200]
    while True:
        stable = True
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if int(t.timee())%6==0:
            a=randint(0,300)
            b = randint(0, 300)

            bbox=[a,b,200,200]

        if len(lmList) != 0:
            lx = bbox[0] + bbox[2]
            ly = bbox[1] + bbox[3]
            x = bbox[0]
            y = bbox[1]
            x, y, w, h, = bbox
            x1, y1 = x + w, y + h
            cv2.line(img, (x, y), (x + 10, y), (255, 0, 230), 20)
            cv2.line(img, (x1 - 10, y1), (x1, y1), (255, 0, 230), 20)
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 255), 2)





            for hand in lmList:
                    if not  (hand[1] >= x and hand[1] <= lx and hand[2] >= y and hand[2] <= ly):
                        stable=False
                        break
            if stable:
                        cv2.putText(img,"Hand is in",(bbox[1],bbox[2]-40),cv2.FONT_HERSHEY_PLAIN,2,(250,120,60),3)
            else :
                        cv2.putText(img, "Hand is not in", (bbox[1],bbox[2]-40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 120, 60), 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(t.timee())), (130, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()


