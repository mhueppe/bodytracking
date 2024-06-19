#
# eye_blink_detection/gui/tabWidget.py
#
# Date: 2024-09-04
# Author: Michael Hüppe
# Project: Eye blink detection
#
import json
import os
from ast import literal_eval
from typing import Dict, Callable

import numpy as np
import pandas as pd
from PySide2.QtCore import QTimer, Signal
# built in
from threading import Lock
# external
from PySide2.QtGui import QImage, QPixmap

from PySide2.QtWidgets import QWidget, QStyle, QFileDialog, QMessageBox, QPushButton, QLineEdit, QVBoxLayout, QDialog, QHBoxLayout
from PySide2.QtCore import Signal as QSignal, QTimer
from PySide2 import QtGui, QtCore
import pyqtgraph as pg
# local
from .src.tabWidget import Ui_Form

mediapipe_body_joints = {
    "nose": 0,
    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,
    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,
    "left_ear": 7,
    "right_ear": 8,
    "mouth_left": 9,
    "mouth_right": 10,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_pinky_1": 17,  # Tip of the left pinky finger
    "right_pinky_1": 18, # Tip of the right pinky finger
    "left_index_1": 19,  # Tip of the left index finger
    "right_index_1": 20, # Tip of the right index finger
    "left_thumb_2": 21,  # Second joint of the left thumb
    "right_thumb_2": 22, # Second joint of the right thumb
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31, # Tip of the left foot
    "right_foot_index": 32  # Tip of the right foot
}
class BodyTrackingWidget(QWidget, Ui_Form):
    _signal_toggleWebcam = QSignal(bool)

    def __init__(
            self, parent=None,
            cb_updateTrackingVisibility: Callable[[dict], None] = lambda trackingSettings: None,
            cb_updateJoint: Callable[[str, int], None] = lambda name, jointIndex: None):
        super().__init__(parent)

        self.history_length = 100
        self._history = np.zeros((self.history_length, 3))
        self._cb_updateTrackingVisibility = cb_updateTrackingVisibility
        self._cb_updateJoint = cb_updateJoint
        self._cameraRunning = True
        self._currentFrame = np.zeros((100, 100, 3))
        self._currentFrame_lock = Lock()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_frame)
        self.setupUi(self)
        self._connectSignalSlots()

    # advanced gui management ###############################################

    def setupUi(self, Form):
        super().setupUi(Form)
        # self.tabWidget.setVisible(False)
        # self.groupBox_xLandmarks.setVisible(False)
        # self.groupBox_yLandmarks.setVisible(False)
        self.comboBox_jointSelection.addItems(list(mediapipe_body_joints.keys()))
        icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        self.pushButton_play.setIcon(icon)
        # Create plot widget
        self.tab_positions.setLayout(QVBoxLayout())
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setYRange(0, 640)
        self.tab_positions.layout().addWidget(self.plotWidget)

        # Set labels
        self.plotWidget.setLabel('left', 'Position', units='pixel')
        self.plotWidget.setLabel('bottom', 'Time', units='s')
        self.plotWidget.setTitle("Nose Position")
        self.plotWidget.addLegend()


        # Plot initial data
        self.plot_x = self.plotWidget.plot(pen='r', name='X')
        self.plot_y = self.plotWidget.plot(pen='b', name='Y')
        self.plot_z = self.plotWidget.plot(pen='g', name='Z')

        self._plots = {}

    def updatePosition(self, pos):
        # Append positions to history

        self._history = np.roll(self._history, -1, axis=0)
        self._history[-1] = pos

        # Update plots
        self.plot_x.setData(y=self._history[:, 0])
        self.plot_y.setData(y=self._history[:, 1])
        self.plot_z.setData(y=self._history[:, 2])


    def _connectSignalSlots(self):
        """
        Connect signal slots of interactive elements
        """
        self._signal_toggleWebcam.connect(
            self._signal_toggleWebcam_handler
        )
        self.pushButton_play.clicked.connect(
            self.pushButton_play_clicked_handler
        )
        self.comboBox_jointSelection.currentTextChanged.connect(
            self.comboBox_jointSelection_currentTextChanged_handler
        )
        for checkBox in [self.checkBox_face, self.checkBox_rightHand, self.checkBox_leftHand, self.checkBox_body]:
            checkBox.stateChanged.connect(
                self.update_trackingVisibility
            )


    def show_frame(self):
        """
        Show the current image in the plot
        :return:
        """
        with self._currentFrame_lock:
            if self._currentFrame is not None:
                image = QImage(self._currentFrame.data, self._currentFrame.shape[1], self._currentFrame.shape[0],
                               QImage.Format_RGB888)
            else:
                return

        pixmap = QPixmap.fromImage(image).scaled(self.label_cameraView.size())
        self.label_cameraView.setPixmap(pixmap)

    def setName(self, name: str):
        """
        Name of the joint currently sending data
        :param name: Name of the joint
        """
        self.plotWidget.setTitle(f"{name} Position")

    def setImage(self, image: np.ndarray):
        """
        Set the current image
        :param image:
        :return:
        """
        with self._currentFrame_lock:
            self._currentFrame = image

    # public handlers
    def handle_toggleWebcam(self, active: bool = True):
        """
        Start the webcam
        """
        self._signal_toggleWebcam.emit(active)

    def comboBox_jointSelection_currentTextChanged_handler(self, text: str):
        """
        Notifies the body tracker which joint to send
        :param text: Select text from the combo box
        """
        self._cb_updateJoint(text, mediapipe_body_joints.get(text, 0))
    def pushButton_play_clicked_handler(self):
        """
        Play or pause the video input
        :return:
        """
        self._cameraRunning = not self._cameraRunning
        self.handle_toggleWebcam(self._cameraRunning)

    def update_trackingVisibility(self):
        """
        Update the Visibility
        :return:
        """
        trackingSettings = {
            "face": self.checkBox_face.isChecked(),
            "rightHand": self.checkBox_rightHand.isChecked(),
            "leftHand": self.checkBox_leftHand.isChecked(),
            "body": self.checkBox_body.isChecked()
        }
        self._cb_updateTrackingVisibility(trackingSettings)
    def _signal_toggleWebcam_handler(self, active: bool):
        """
        Play or stop the webcam
        :param active: Whether to play or stop the webcam
        :return:
        """
        icon = self.style().standardIcon(QStyle.SP_MediaPause if active else QStyle.SP_MediaPlay)
        self.pushButton_play.setIcon(icon)
        if active:
            self.timer.start(1000 / 60)  # 30 FPS
        else:
            self.timer.stop()  # 30 FPS
