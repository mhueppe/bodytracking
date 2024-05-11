# author: Michael Hüppe
# date: 08.05.2024
# project: bodyTracking_widget/bodyTracker.py
# built-in
from threading import Event, Thread, Lock
from typing import Callable

import mediapipe as mp
import cv2
import numpy as np
from .distributor import Distributor


class BodyTracker:
    FACE = 0x00
    LEFT_HAND = 0x01
    RIGHT_HAND = 0x02
    BODY = 0x03

    def __init__(self,
                 cb_sendBodyImage: Callable[[np.ndarray], None] = lambda image: None,
                 cb_sendBodyPositions: Callable[[np.ndarray, np.ndarray], None] = lambda face_pos, body_pos: None,
                 cameraIndex: int = 0):
        self._cameraIndex: int = cameraIndex
        self._h = None
        self._w = None
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

    def trackBody_cont(self):
        """
        Tracks the body using the video input from the webcam
        :return:
        """
        with self._mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while self._continueTracking.is_set():
                # Initiate holistic model
                ret, frame = self._cap.read()

                # Recolor Feed
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Make Detections
                results = holistic.process(image)
                # print(results.face_landmarks)

                # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
                for bodyPart, code, plot in zip([results.right_hand_landmarks,
                                           results.left_hand_landmarks,
                                           results.pose_world_landmarks],
                                                [self.RIGHT_HAND, self.LEFT_HAND, self.BODY],
                                                [ "rightHand", "leftHand", "face"]):
                    if bodyPart:
                        pose = np.asarray([[l.x, l.y, l.z] for l in bodyPart.landmark],
                                          dtype=np.float32)
                        self._cb_sendBodyPositions(plot, np.mean(pose, axis=0))
                        pose = (np.asarray((self._w, self._h, 0)) - pose) * 50
                        self._distributor.sendData(code.to_bytes(1, "little") + pose.astype(np.float32).tobytes())

                self.showPredictions(image, results)


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
            success, img = self._cap.read()
            self._h, self._w, _ = img.shape
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
