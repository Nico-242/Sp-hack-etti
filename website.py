from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

touchTimes = [0,0,0,0,0]

camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    tracker = handTracker()

    fingerTaps = 0
    previousIndex = -1
    #touchTimes
    touchFinger = ["Finger Taps","Power Grip","Wrist Flex","Finger Stretch", "Thumb Stretch"]

    while True:
        # Capture frame-by-frame
        success, image = camera.read()  # read the camera frame
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)

        if not success:
            break
        else:
            if len(lmList) != 0:
                if ((abs(lmList[0][2] - lmList[8][2]) < 150) and (abs(lmList[0][1] - lmList[8][1]) < 150)) and ((abs(lmList[0][2] - lmList[12][2]) < 150) and (abs(lmList[0][1] - lmList[12][1]) < 150)) and ((abs(lmList[0][2] - lmList[16][2]) < 105) and (abs(lmList[0][1] - lmList[16][1]) < 150)) and ((abs(lmList[0][2] - lmList[20][2]) < 150) and (abs(lmList[0][1] - lmList[20][1]) < 150)):
                    print("PALM")
                    previousIndex = 1
                elif ((abs(lmList[8][1] - lmList[12][1]) > 130) and (abs(lmList[12][1] - lmList[16][1]) > 130) and (abs(lmList[16][1] - lmList[20][1]) > 130)):
                    print("Finger Stretch")
                    previousIndex = 3
                elif ((abs(lmList[4][2] - lmList[17][2]) < 50) and (abs(lmList[4][1] - lmList[17][1]) < 50)):
                    print("Thumb Stretch")
                    previousIndex = 4
                elif (lmList[0][2] - lmList[4][2]) < 50:
                    print("WRIST FLEX")
                    previousIndex = 2
                elif (abs(lmList[8][2] - lmList[4][2]) < 50) and (abs(lmList[8][1] - lmList[4][1]) < 50):
                    print("INDEX")
                    fingerTaps = 1
                elif (abs(lmList[12][2] - lmList[4][2]) < 50) and (abs(lmList[12][1] - lmList[4][1]) < 50):
                    print("MIDDLE")
                    if (fingerTaps == 1):
                        fingerTaps = 2
                    else:
                        previousIndex = -1
                elif (abs(lmList[16][2] - lmList[4][2]) < 50) and (abs(lmList[16][1] - lmList[4][1]) < 50):
                    print("RING")
                    if (fingerTaps == 2):
                        fingerTaps = 3
                    else:
                        previousIndex = -1
                elif (abs(lmList[20][2] - lmList[4][2]) < 70) and (abs(lmList[20][1] - lmList[4][1]) < 70):
                    print("PINKY")
                    if (fingerTaps == 3):
                        previousIndex = 0
                    else:
                        previousIndex = -1
                else:
                    if previousIndex >= 0:
                        touchTimes[previousIndex]  = touchTimes[previousIndex] + 1
                        print(touchFinger[previousIndex] + ": " + str(touchTimes[previousIndex]))
                    previousIndex = -1
                    print("NOT TOUCHING")
                complete = True
                for element in touchTimes:
                    if element < 10:
                        complete = False
                #if complete:
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/update')
def get_update():
    return touchTimes

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    
    def positionFinder(self,image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            #if draw:
                cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)
        return lmlist

if __name__ == '__main__':
    app.run()