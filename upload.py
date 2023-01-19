import json

from datetime import time
from random import randint

import HandTrackingModule
import PoseModule as Pose
import FaceMeshModule


import werkzeug.utils
from flask import Flask , jsonify,request
import cv2

import FaceModule
from HandTrackingModule import handDetector
from Timer import Timer
import time
response=""
def readImg(image,x,y):
        t = Timer()
        t.start()
        x=int(float(x))
        y=int(float(y))
        pTime = 0
        cTime = 0
    #    cap = cv2.VideoCapture(image)

        detector = handDetector()
        drawRec = FaceModule.FaceDetection

        firstIn = False

        bbox = [50, 100, 100, 100]

        stable=True
        #success, img = cap.read()
        img=cv2.imread(image)
        width = int(360)
        height = int(640)
        dim = (width, height)

        # resize image
        img = cv2.resize(img, dim)

        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if int(t.timee()) % 3 == 0:
            a = randint(0, 300)
            b = randint(0, 300)

            bbox = [x,y, 100, 100]
            print ("x",x)
            print("y", y)

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
                if not (hand[1] >= x and hand[1] <= lx and hand[2] >= y and hand[2] <= ly):
                    stable = False
                    break
            if stable:
                cv2.putText(img, "Hand is in", (bbox[1], bbox[2] - 40), cv2.FONT_HERSHEY_PLAIN, 2, (250, 120, 60), 3)
            else:
                cv2.putText(img, "Hand is not in", (bbox[1], bbox[2] - 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 120, 60), 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime)

        pTime = cTime
        cv2.putText(img, str(int(t.timee())), (130, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        return stable


def figit(image):
    t = Timer()
    t.start()
    pTime=1
    pose = Pose.poseDetector()
    hand = HandTrackingModule.handDetector()
    face = FaceMeshModule.FaceMesh()
    faceD = FaceModule.FaceDetection()
    bol = False
    count = 0
    counter = 0
    isOUt = False
    mesh = FaceMeshModule.FaceMesh()

    counter1 = 0
    counter = 0
    bol = True
    firstIn = False
    stable = False

    box = [100, 200, 100, 100]
    while True:
        img=cv2.imread(image)
        img = hand.findHands(img)
        handLand = hand.findPosition(img)
        lx = box[0] + box[2]
        ly = box[1] + box[3]
        x = box[0]
        y = box[1]
        if 1 < 40:

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
                #angle = pose.angleDetection(img, 11, 13, 15)
                #percentage = np.interp(angle, (170, 30), (0, 100))
                cv2.putText(img, str(int(t.timee())), (130, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
                counter1, isOUt = pose.figit(img, counter1, isOUt)
                cv2.putText(img, "Test 1", (330, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)


        elif t.timee() > 80:
            cv2.putText(img, "you Have Blinked: " + str(int(counter)) + " Times", (10, 280), cv2.FONT_HERSHEY_PLAIN, 3,
                       (0, 240, 230), 4)
            cv2.putText(img, "you Have Figited: " + str(int(counter1)) + " Times", (10, 380), cv2.FONT_HERSHEY_PLAIN, 3,
                       (0, 240, 230), 3)
            if counter + counter1 * 2 > 50:
                result = " may bave Autism "
            else:
                result = " dont have Autism "

            cv2.putText(img, "you : " + result, (10, 420), cv2.FONT_HERSHEY_PLAIN, 3, (0, 240, 230), 3)


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

                    cv2.putText(img, str(counter), (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 135, 40), 2)
                    cv2.putText(img, str(int(t.timee())), (100, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)
                    cv2.putText(img, "Test 2", (330, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 240, 230), 4)

        # faceD.fancyDraw(img,bbox=box)

        ###

        cTime = time.time()

        fps = 1 / (cTime - pTime)

        pTime = cTime
        cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 155), 2)

        cv2.imshow("Trainer", img)
        cv2.waitKey(1)

print(cv2.__version__)

app=Flask (__name__)
@app.route('/upload',methods=["GET","POST"])
def upload():
    global response
    if(request.method=="POST"):
        imagefile=request.files['file']


        filename=werkzeug.utils.secure_filename(imagefile.filename)
        img=imagefile.save("imaaaaaaaage.jpg")
        #print(request.json['id'])
        x=request.form.get('x')
        y = request.form.get('y')


        response=readImg("imaaaaaaaage.jpg",x,y)# process hand and return if it is in or out of the box
        #figit("imaaaaaaaage.jpg")
        print(response)




        return jsonify({
            "message":"Image Uploaded"
        })
    else :
        return jsonify({"name": f"{response}"})#return the response

@app.route('/result',methods=["GET","POST"])
def nameRoute():
    global  response
    #global r



    if (request.method=="POST"):
        request_data=request.data
        request_data=json.loads(request_data.decode(("utf-8")))

        resutl=request_data['result']
        print("xxxx",resutl)


        response =  f" C'est possible que vous aveza {response}"
        #print (response)
        response=resutl
    else :
        print(jsonify({"name":response}))
        return jsonify({"name":f"{response}"})
if __name__ =="__main__":
    app.run()

'''' if angle <= 30:
             if not bol:
                 count += 0.5
              bol = True
         elif angle >= 160:
             if bol:
                 count += 0.5
                 bol = False
        '''
