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


class BodyTrackingWidget(QWidget, Ui_Form):
    _signal_toggleWebcam = QSignal(bool)

    def __init__(
            self, parent=None, cb_updateTrackingVisibility: Callable[[dict], None] = lambda trackingSettings: None):
        super().__init__(parent)

        self.history_length = 100
        self.face_history = np.zeros((self.history_length, 3))
        self.rightHand_history = np.zeros((self.history_length, 3))
        self.leftHand_history = np.zeros((self.history_length, 3))
        self._cb_updateTrackingVisibility = cb_updateTrackingVisibility
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
        self.groupBox_xLandmarks.setVisible(False)
        self.groupBox_yLandmarks.setVisible(False)
        icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        self.pushButton_play.setIcon(icon)
        # Create plot widget
        self.tab_positions.setLayout(QVBoxLayout())
        self.plotWidget_face = pg.PlotWidget()
        self.plotWidget_rightHand = pg.PlotWidget()
        self.plotWidget_leftHand = pg.PlotWidget()
        self.plotWidget_rightHand.setMaximumHeight(200)
        self.plotWidget_leftHand.setMaximumHeight(200)
        self.plotWidget_face.setMaximumHeight(200)
        self.tab_positions.layout().addWidget(self.plotWidget_face)
        self.tab_positions.layout().addWidget(self.plotWidget_rightHand)
        self.tab_positions.layout().addWidget(self.plotWidget_leftHand)

        # Set labels
        self.plotWidget_face.setLabel('left', 'Position', units='m')
        self.plotWidget_face.setLabel('bottom', 'Time', units='s')
        self.plotWidget_face.setTitle("Face Position")
        self.plotWidget_face.addLegend()

        self.plotWidget_rightHand.setLabel('left', 'Position', units='m')
        self.plotWidget_rightHand.setLabel('bottom', 'Time', units='s')
        self.plotWidget_rightHand.setTitle("Right Hand Position")
        self.plotWidget_rightHand.addLegend()

        self.plotWidget_leftHand.setLabel('left', 'Position', units='m')
        self.plotWidget_leftHand.setLabel('bottom', 'Time', units='s')
        self.plotWidget_leftHand.setTitle("Left Hand Position")
        self.plotWidget_leftHand.addLegend()


        # Plot initial data
        self.face_plot_x = self.plotWidget_face.plot(pen='r', name='X')
        self.face_plot_y = self.plotWidget_face.plot(pen='b', name='Y')
        self.face_plot_z = self.plotWidget_face.plot(pen='g', name='Z')

        self.rightHand_plot_x = self.plotWidget_rightHand.plot(pen='r', name='X')
        self.rightHand_plot_y = self.plotWidget_rightHand.plot(pen='b', name='Y')
        self.rightHand_plot_z = self.plotWidget_rightHand.plot(pen='g', name='Z')

        self.leftHand_plot_x = self.plotWidget_leftHand.plot(pen='r', name='X')
        self.leftHand_plot_y = self.plotWidget_leftHand.plot(pen='b', name='Y')
        self.leftHand_plot_z = self.plotWidget_leftHand.plot(pen='g', name='Z')

        self._plots = {}
        self._plots["face"] = (self.face_plot_x, self.face_plot_y, self.face_plot_z)
        self._plots["rightHand"] = (self.rightHand_plot_x, self.rightHand_plot_y, self.rightHand_plot_z)
        self._plots["leftHand"] = (self.leftHand_plot_x, self.leftHand_plot_y, self.leftHand_plot_z)
        self._histories = {}
        self._histories["face"] = self.face_history
        self._histories["rightHand"] = self.rightHand_history
        self._histories["leftHand"] = self.leftHand_history


    def updatePosition(self, plot, pos):
        # Append positions to history
        x_plot, y_plot, z_plot = self._plots[plot]

        self._histories[plot] = np.roll(self._histories[plot], -1, axis=0)
        self._histories[plot][-1] = pos

        # Update plots
        x_plot.setData(y=self._histories[plot][:, 0])
        y_plot.setData(y=self._histories[plot][:, 1])
        z_plot.setData(y=self._histories[plot][:, 2])


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
