# author: Michael Hüppe
# date: 08.05.2024
# project: bodyTracking_widget/bodyTracker.py
# built-in
from threading import Event, Thread, Lock
from typing import Callable, Union
import mmap

import mediapipe as mp
import cv2
import numpy as np
from .distributor import Distributor


class BodyTracker:
    FACE = 0x00
    LEFT_HAND = 0x01
    RIGHT_HAND = 0x02
    BODY = 0x03
    IMAGE = 0x04

    def __init__(self,
                 cb_sendBodyImage: Callable[[np.ndarray], None] = lambda image: None,
                 cb_sendBodyPositions: Callable[[np.ndarray], None] = lambda positions: None,
                 cameraIndex: Union[int, str] = 0):
        self._jointIndex = 0
        self._results = None
        self._cameraIndex: int = cameraIndex
        self._h = 480
        self._w = 640
        self._show_face = True
        self._show_rightHand = True
        self._show_leftHand = True
        self._show_body = True
        self._cb_sendBodyImage = cb_sendBodyImage
        self._cb_sendBodyPositions = cb_sendBodyPositions
        self._cap = None
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_holistic = mp.solutions.holistic
        self._bodyTrackingThread: Thread = None
        self._continueTracking: Event = Event()
        self.startTracking()
        self._distributor = Distributor()
        self.shm = mmap.mmap(-1, self._w * self._h * 3, "shared_memory")

        self._track = True

    def trackBody_cont(self):
        """
        Tracks the body using the video input from the webcam
        :return:
        """
        with self._mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while self._continueTracking.is_set():
                # Initiate holistic model
                ret, frame = self._cap.read()
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Recolor Feed
                # Make Detections
                self._results = results = holistic.process(image)
                # print(results.face_landmarks)
                self.shm.write(cv2.flip(image, 0).tobytes())

                # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
                for bodyPart, code, plot in zip([results.right_hand_landmarks,
                                                 results.left_hand_landmarks,
                                                 results.pose_landmarks],
                                                [self.RIGHT_HAND, self.LEFT_HAND, self.BODY],
                                                ["rightHand", "leftHand", "pose"]):
                    if bodyPart and plot == "pose":
                        for i, landmark in enumerate(bodyPart.landmark):
                            color = (255, 0, 0) if i != self._jointIndex else (0, 255, 0)
                            size = 2 if i != self._jointIndex else 5
                            landmark = int(landmark.x * self._w), int(landmark.y * self._h), int(landmark.z * 10)
                            image = cv2.circle(image, (landmark[0], landmark[1]), size, color, -1)
                            if i == self._jointIndex:
                                self._cb_sendBodyPositions(np.asarray(landmark))

                        # converted = self.convert_to_relative(bodyPart.landmark, image.shape[0], image.shape[1])[0]
                        # print(bodyPart.landmark[20].x * self._w)
                        pose = np.asarray([[int(landmark.x * self._w), int(landmark.y * self._h), int(landmark.z * 10)]
                                          for landmark in bodyPart.landmark])

                        self._distributor.sendData(code.to_bytes(1, "little") + pose.astype(np.int16).tobytes())
                self.shm.seek(0)
                self._cb_sendBodyImage(image)

                # self.showPredictions(image, results)

    @staticmethod
    def convert_to_relative(landmarks, image_width, image_height):
        relative_landmarks = []
        for lm in landmarks:
            # Normalize the coordinates
            x_norm = lm.x / image_width
            y_norm = lm.y / image_height

            # Adjust range to [-1, 1]
            x_rel = 2 * x_norm - 1
            y_rel = 2 * y_norm - 1

            relative_landmarks.append((x_rel, y_rel))

        return relative_landmarks

    def showPredictions(self, image, results):
        # # 1. Draw face landmarks
        if self._show_face:
            self._mp_drawing.draw_landmarks(image, results.face_landmarks,
                                            self._mp_holistic.FACEMESH_TESSELATION,
                                            self._mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1,
                                                                         circle_radius=1),
                                            self._mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1,
                                                                         circle_radius=1)
                                            )

        # 2. Right hand
        if self._show_rightHand:
            self._mp_drawing.draw_landmarks(image, results.right_hand_landmarks,
                                            self._mp_holistic.HAND_CONNECTIONS,
                                            self._mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2,
                                                                         circle_radius=4),
                                            self._mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2,
                                                                         circle_radius=2)
                                            )

        # 3. Left Hand
        if self._show_leftHand:
            self._mp_drawing.draw_landmarks(image, results.left_hand_landmarks,
                                            self._mp_holistic.HAND_CONNECTIONS,
                                            self._mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2,
                                                                         circle_radius=4),
                                            self._mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2,
                                                                         circle_radius=2)
                                            )

        # 4. Pose Detections
        if self._show_body:
            self._mp_drawing.draw_landmarks(image, results.pose_landmarks, self._mp_holistic.POSE_CONNECTIONS,
                                            self._mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2,
                                                                         circle_radius=4),
                                            self._mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2,
                                                                         circle_radius=2)
                                            )

        self._cb_sendBodyImage(image)

    def setJoint(self, jointIndex: int):
        """
        Change the joint to send data to the visualilzer
        :param jointIndex: Index of the joint to send
        """
        self._jointIndex = jointIndex

    def setTrackingVisibility(self, settings: dict):
        """
        Update view settings
        :param settings: which track points should be visible and which not
        :return:
        """
        self._show_face = settings.get("face", True)
        self._show_rightHand = settings.get("rightHand", True)
        self._show_leftHand = settings.get("leftHand", True)
        self._show_body = settings.get("body", True)

    def startTracking(self):
        """
        Start the tracking Process
        :return:
        """
        self._continueTracking.set()
        if self._cap is None:
            self._cap = cv2.VideoCapture(self._cameraIndex)
            self._cap.set(3, self._w)
            self._cap.set(4, self._h)
            success, img = self._cap.read()

            self._h, self._w, _ = img.shape
            print(self._h, self._w)
        if self._bodyTrackingThread is None:
            self._bodyTrackingThread = Thread(target=self.trackBody_cont)
            self._bodyTrackingThread.start()

    def stopTracking(self):
        """
        Stop the tracking process
        :return:
        """
        self._continueTracking.clear()
        if self._bodyTrackingThread:
            self._bodyTrackingThread.join()
            self._bodyTrackingThread = None

        if self._cap:
            self._cap.release()
            self._cap = None
            cv2.destroyAllWindows()
