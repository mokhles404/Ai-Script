import cv2 as cv
import time
#pTime=0
import mediapipe as mp
class FaceDetection():
    def __init__(self,minDetectionCon=0.98):
        self.minDetectionCon=minDetectionCon

        self.mpFaceDetect = mp.solutions.face_detection
        self.face = self.mpFaceDetect.FaceDetection(minDetectionCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findFaces(self,img,draw=True ):
        bboxs=[]
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.face.process(imgRGB)
        if self.results.detections:

            for id, detection in enumerate(self.results.detections):
                # mpDraw.draw_detection(img,detection)
                # print(detection.score)
                # print(detection.location_data.relative_bounding_box)
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin
                                                * h), \
                       int(bboxC.width * w), int(bboxC.height * h)
                img=self.fancyDraw(img,bbox)####Even Methods needs to be referenced with (self)
                cv.putText(img, f"conf:{int(detection.score[0] * 100)}%", (bbox[0] - 10, bbox[1] - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                bboxs.append([id,bbox,detection.score])


        return img,bboxs


    def fancyDraw (self,img,bbox,l=30,t=10):
        x,y,w,h,=bbox
        x1,y1=x+w,y+h
        cv.line(img,(x,y),(x+l,y),(255,0,230),t)
        cv.line(img, (x1-l, y1), (x1,y1), (255, 0, 230), t)
        cv.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 255), 2)
        return img


def main():
    cap=cv.VideoCapture(0)
    pTime=0
    faceDetect=FaceDetection()

    while True:
        succes,img=cap.read()
        img,lst=faceDetect.findFaces(img)
        print(lst)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, "fps" + str(int(fps)), (30, 70), cv.FONT_ITALIC, 1, (0, 255, 0), 2)
        cv.imshow("img", img)
        cv.waitKey(1)  # speed increased
#####
if __name__=="__main__":
    main()