import cv2
import mediapipe as mp

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

def main():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()

    previousIndex = -1
    touchTimes = [0,0,0,0, 0]
    touchFinger = ["Index","Middle","Ring","Pinky", "All"]

    while True:
        success,image = cap.read()
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        if len(lmList) != 0:
            if ((abs(lmList[0][2] - lmList[8][2]) < 150) and (abs(lmList[0][1] - lmList[8][1]) < 150)) and ((abs(lmList[0][2] - lmList[12][2]) < 120) and (abs(lmList[0][1] - lmList[12][1]) < 120)) and ((abs(lmList[0][2] - lmList[16][2]) < 120) and (abs(lmList[0][1] - lmList[16][1]) < 120)) and ((abs(lmList[0][2] - lmList[20][2]) < 150) and (abs(lmList[0][1] - lmList[20][1]) < 150)):
                print("PALM")
                previousIndex = 4
            elif (abs(lmList[8][2] - lmList[4][2]) < 50) and (abs(lmList[8][1] - lmList[4][1]) < 50):
                #print("INDEX")
                previousIndex = 0
            elif (abs(lmList[12][2] - lmList[4][2]) < 50) and (abs(lmList[12][1] - lmList[4][1]) < 50):
                #print("MIDDLE")
                previousIndex = 1
            elif (abs(lmList[16][2] - lmList[4][2]) < 50) and (abs(lmList[16][1] - lmList[4][1]) < 50):
                #print("RING")
                previousIndex = 2
            elif (abs(lmList[20][2] - lmList[4][2]) < 70) and (abs(lmList[20][1] - lmList[4][1]) < 70):
                #print("PINKY")
                previousIndex = 3
            else:
                if previousIndex >= 0:
                    touchTimes[previousIndex]  = touchTimes[previousIndex] + 1
                    print(touchFinger[previousIndex] + " finger touches: " + str(touchTimes[previousIndex]))

                previousIndex = -1
                #print("NOT TOUCHING")

            

        cv2.imshow("Video",image)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()