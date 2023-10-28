# importing the opencv module  
import cv2  
import matplotlib.pyplot as plt
import numpy as np
import sys

# using imread('path') and 1 denotes read as  color image  
# img = cv2.imread('dog.jpeg',1)  

# This is using for display the image  
# # cv2.imshow('image',img)  
# img_BGR = cv2.imread('dog.jpeg', cv2.IMREAD_COLOR)
# b, g, r = cv2.split(img_BGR)

# plt.figure(figsize=[20,5])
# plt.subplot(141);plt.imshow(r,cmap='gray');plt.title('Red Channel')
# plt.subplot(142);plt.imshow(g,cmap='gray');plt.title('Green Channel')
# plt.subplot(143); plt.imshow(b,cmap='gray');plt.title('Blue CHannel')

# imgMerged = cv2.merge((b,g,r))
# plt.subplot(144);plt.imshow(imgMerged[:,:,::-1]);plt.title("Merged Output");
# plt.show()

# s = 0
# if(len(sys.argv) > 1) :
#     s = sys.argv[1]

# source = cv2.VideoCapture(s)

# win_name = 'Camera Preview'
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# while cv2.waitKey(1) != 27:
#     has_frame,frame = source.read()
#     if not has_frame:
#         break
#     cv2.imshow(win_name, frame)

# source.release()
# cv2.waitKey(0)
# cv2.destroyAllWindow()

# # cv2.waitKey() # This is necessary to be required so that the image doesn't close immediately.  
# # # It will run continuously until the key press.  
# # cv2.destroyAllWindows() 



import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #if id == 20 :
                cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
    cv2.imshow("Output", image)
    cv2.waitKey(1)
