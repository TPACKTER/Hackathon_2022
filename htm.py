import cv2 as cv
import mediapipe as mp
import time
###import speech_recognition as sr
import socket

host = '127.0.0.1'  # as both code is running on same pc
port = 6000  # socket server port number
##client_socket = socket.socket()  # instantiate

# Define currently used camera
USEDCAMERA = 0
# Define camera width and height
CAMWIDTH = 640
CAMHEIGHT = 480
# Define text color
TEXTCOLOR = (100, 150, 210)


# The hand detector model class.
# Initialize with empty parenthesis or pass the desired values in the object initialization.
# The arguments passed are the arguments needed to create the mediapipe Hands model
class HandDetector:
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=2,
                 model_complexity=1,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.results = None
        self.mode = static_image_mode
        self.max_hands = max_num_hands
        self.complexity = model_complexity
        self.minimal_detection_confidence = min_detection_confidence
        self.minimal_tracking_confidence = min_tracking_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.complexity,
                                         self.minimal_detection_confidence,
                                         self.minimal_tracking_confidence)  # Create a mediapipe Hands class object.
        self.mp_draw_utility = mp.solutions.drawing_utils  # Create a mediapipe drawing utility to draw the points

    # find_hands() takes a frame, activates mediapipe's hand tracking algorithm and returns the frame with the hands
    # marked (points and connecting lines). As default the 'draw' argument is set to 'True'. Set to 'False' to cancel
    # drawing the points and lines on the frame.
    def find_hands(self, frame, draw=True):
        rgb_frame = cv.cvtColor(frame,  # Convert the image to RGB. mediapipe uses RGB images
                                cv.COLOR_BGR2RGB)  # and open-cv uses BGR images.
        self.results = self.hands.process(rgb_frame)  # Process the frame using the Hands.process() method
        if self.results.multi_hand_landmarks:  # If True, a hand or more were found. Else equals to None
            for hand in self.results.multi_hand_landmarks:  # Loop through the found hands and perform actions on each
                if draw:
                    self.mp_draw_utility.draw_landmarks(frame, hand,  # Draw the 21 points
                                                        self.mp_hands.HAND_CONNECTIONS)  # and the connecting lines
                    # on each hand
        return frame

    # find_position() takes a frame and the hand number to be processed (set as default to '0' - the first hand in
    # the list), finds the position of each point and returns that list
    def find_landmarks(self, frame, hand_number=USEDCAMERA):
        landmarks = []
        if self.results.multi_hand_landmarks:  # If True, a hand or more were found. Else equals to None
            hand = self.results.multi_hand_landmarks[hand_number]
            for index, landmark in enumerate(hand.landmark):  # Match the index of the landmark to the landmark
                frame_height, frame_width, channels = frame.shape
                center_x, center_y = int(landmark.x * frame_width), int(landmark.y * frame_height)
                landmarks.append([index, center_x, center_y])
        return landmarks
    # def findPosition(self, img, handNo=0, draw=True):
    #     lmList = []
    #     if self.results.multi_hand_landmarks:
    #         myHand = self.results.multi_hand_landmarks[handNo]
    #         for id, lm in enumerate(myHand.landmark):
    #             # print(id, lm)
    #             h, w, c = img.shape
    #             cx, cy = int(lm.x * w), int(lm.y * h)
    #             # print(id, cx, cy)
    #             lmList.append([id, cx, cy])
    #             if draw:
    #                 cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
    #
    #     return lmList


    def run(self, camera):
        num_frames = 1

        while True:
            print(num_frames)
            ret, depth_frame, color_frame = camera.get_frame()

            frame = self.find_hands(color_frame)
            self.find_landmarks(frame)#finding landmarks
            print(ret)
            if ret:  # If a frame exists
                cv.imshow('Camera', frame)  # Display the current frame (BGR frame)
                #detector = self.handDetector(detectionCon=0.75)
                #detector = HandDetector()
            # ############ X Y Z ###########################
                lmList = self.find_landmarks(frame,0)
                print("lmList")


                if num_frames%25 == 0:
                    try:
                        print(str(lmList[8]))
                        x = lmList[8][1]
                        x = float(x - 100) / (1000 - 100) * (10 - (-10)) + (-10)

                        z = lmList[8][2]
                        z = float(z - 0) / (500 - 0) * (80 - 65) + 65

                        y = 30

                        message = str(x) + "," + str(y) + "," + str(z) + '\n'
                        print(message)

                        cv.putText(frame, "COMPUTER", (10, 100),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.9,
                                   (255, 193, 43), 2)
                        client_socket = socket.socket()  # instantiate   ????? instead of UP

                        client_socket.connect((host, port))  # connect to the server
                        client_socket.send(message.encode())  # send message
                        data = client_socket.recv(1024)  # receive response
                        print('Received from server: ' + data.decode())  # show in terminal
                        client_socket.close()  # close the connection
                    except:
                        print("was'nt able to find coordinates")


                print("update num_frames")
                if num_frames == 24:
                    num_frames = 0
                else:
                    num_frames += 1


                if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' key to stop and exit
                    break


                '''
                s = sr.Recognizer()
                #with sr.AudioFile("word.wav") as source:#by preperd audio
                with sr.Microphone() as source:
                    s.adjust_for_ambient_noise(source)
                    audio = s.listen(source)
                    try:
                        text = s.recognize_google(audio)
                        if ('yes' in text):
                            print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
                            print(str(lmList[8]))
                            x = lmList[8][1]
                            x = float(x-100)/(1000-100)*(10-(-10))+(-10)
                            #print(str(x.dtype))
                            ##print(str(x))
                            y = lmList[8][2]
                            y = float(y - 0) / (500 - 0) * (80 - 65) + 65
                            ##print(str(y))
                            z =lmList[8][0]
                            ##print(str(z))
                            ##print(str(depth_frame))
                            #cv.putText(frame, )

                            message = str(x) + "," + str(30) + "," + str(y) + '\n'
                            print(message)

                            cv.putText(frame, "COMPUTER", (10, 100),
                                        cv.FONT_HERSHEY_SIMPLEX, 0.9,
                                        (255, 193, 43), 2)
                            ######client_socket = socket.socket()  # instantiate   ????? instead of UP

                            client_socket.connect((host, port))  # connect to the server
                            client_socket.send(message.encode())  # send message
                            data = client_socket.recv(1024)  # receive response
                            print('Received from server: ' + data.decode())  # show in terminal
                            client_socket.close()  # close the connection

                    except:
                         print("was'nt able to find coordinates")
            ####################################
                if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' key to stop and exit
                    break
                    '''
            else:  # No frame exists, break the loop
                break


        cv.destroyAllWindows()