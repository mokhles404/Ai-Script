import cv2 as cv
import mediapipe as mp
import time


class FaceMesh():
    def __init__(self, static_image_mode=False,
               max_num_faces=1,
               refine_landmarks=False,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.refine_landmarks =refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        #######
        self.mpDraw = mp.solutions.drawing_utils
        self.mpMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpMesh.FaceMesh(max_num_faces=2)
        self.drawSpecs = self.mpDraw.DrawingSpec(thickness=1, color=(255, 60, 120), circle_radius=1)



    def getMesh(self,img,draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)
        faces=[]

        if self.results.multi_face_landmarks:
            for face_landmark in self.results.multi_face_landmarks:

                if draw:
                     self.mpDraw.draw_landmarks(img, face_landmark, self.mpMesh.FACEMESH_CONTOURS, self.drawSpecs, self.drawSpecs)
                face=[]
                for id, lm in enumerate(face_landmark.landmark):
                    # print(lm)
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    face.append([id,x,y])
                    #cv.putText(img, str(id), (x,y), cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)

                faces.append(face)

        return img,faces







def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    facemesh=FaceMesh()
    while True:
        succes, img = cap.read()
        #imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img,result=facemesh.getMesh(img)
        print(result)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (20, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        cv.imshow("Video", img)
        cv.waitKey(1)


################
if __name__=="__main__":
    main()
