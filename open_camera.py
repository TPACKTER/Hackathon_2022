import pyrealsense2 as rs
import numpy as np
import cv2 as cv
import speech_recognition as sr
import mediapipe as mp
import time
from LIDAR_Object import LIDAR_Object

cam = LIDAR_Object()#camera obj created
# counter = 0

# def save_frame(event, x, y, args, params):
#     if event == cv.EVENT_LBUTTONDOWN:
#         global counter
#         global img
#         for i in range(10):
#             counter+=1
#             print('Click')
#             cv.imwrite(str(counter)+'.jpg', img)
#
# # Create mouse event
# cv.namedWindow("Color frame")
# cv.setMouseCallback("Color frame", save_frame)
#
# while True:
#     ret, depth_frame, color_frame = cam.get_frame()
#     img = color_frame
#     cv.imshow("depth frame", depth_frame)
#     cv.imshow("Color frame", color_frame)
#     key = cv.waitKey(1)
#     if key == 27:
#         cv.destroyAllWindows()
#         break
# #distance markdowm ####################################################################################
# point = (400, 300)
#
# def show_distance(event, x, y, args, params):
#     global point
#     point = (x, y)
#
# # Create mouse event
# cv.namedWindow("Color frame")
# cv.setMouseCallback("Color frame", show_distance)
#
# while True:
#     ret, depth_frame, color_frame = cam.get_frame()
#
#     # Show distance for a specific point
#     cv.circle(color_frame, point, 4, (0, 0, 255))
#     distance = depth_frame[point[1], point[0]]
#
#     cv.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
#
#     cv.imshow("depth frame", depth_frame)
#     cv.imshow("Color frame", color_frame)
#     key = cv.waitKey(1)
#     if key == 27:
#         cv.destroyAllWindows()
#         break
from htm import HandDetector
#cap = cv.VideoCapture(0)
#detector = HandDetector()
htm = HandDetector()#detecting the hand base
#print("hey")
htm.run(cam)

#detector.run(cam)
  ###################################################################################
#
# tipIds = [4, 8, 12, 16, 20]
#
# while True:
#     #success, img = cap.read()
#     img = htm.findHands(img)
#     lmList = htm.find_landmarks(img, draw=False)
#
#     if len(lmList) != 0:
#         fingers = []
#
#         # Thumb
#         if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
#             fingers.append(1)
#         else:
#             fingers.append(0)
#
#         # 4 Fingers
#
#             if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
#                 fingers.append(1)
#             else:
#                 fingers.append(0)
#
#         print(fingers)
#         totalFingers = fingers.count(1)
#         print(totalFingers)
#       #  self.mpDraw.draw_landmarks(img, handLms,
#        #                            self.mpHands.HAND_CONNECTIONS)
#
# ##pose track#######################################################################################
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_pose = mp.solutions.pose
#
#
# with mp_pose.Pose(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5, enable_segmentation=True) as pose:
#     while True:
#         success, depth, image = cam.get_frame()
#         if not success:
#             break
#
#         # To improve performance, optionally mark the image as not writeable to
#         # pass by reference.
#         image.flags.writeable = False
#         image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
#         results = pose.process(image)
#
#         # Draw the pose annotation on the image.
#         image.flags.writeable = True
#         image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
#         mp_drawing.draw_landmarks(
#             image,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS,
#             landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#         # Flip the image horizontally for a selfie-view display.
#         cv.imshow('MediaPipe Pose', cv.flip(image, 1))
#         if cv.waitKey(5) & 0xFF == 27:
#             cv.destroyAllWindows()
#             break
#
# ##############################################
#         def audio_call():
#             s = sr.Recognizer()
#             with sr.Microphone as source:
#                 audio = sr.listen(source)
#                 text = sr.recognize_google(audio)
#                 print(text)
#
