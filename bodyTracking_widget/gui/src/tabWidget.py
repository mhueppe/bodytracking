# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(874, 891)
        self.horizontalLayout_4 = QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_cameraView = QLabel(Form)
        self.label_cameraView.setObjectName(u"label_cameraView")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_cameraView.sizePolicy().hasHeightForWidth())
        self.label_cameraView.setSizePolicy(sizePolicy)
        self.label_cameraView.setMinimumSize(QSize(300, 300))
        self.label_cameraView.setMaximumSize(QSize(3000, 3000))

        self.horizontalLayout_4.addWidget(self.label_cameraView)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tab_positions = QWidget()
        self.tab_positions.setObjectName(u"tab_positions")
        self.verticalLayout_4 = QVBoxLayout(self.tab_positions)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_2 = QFrame(self.tab_positions)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBox_jointSelection = QComboBox(self.frame_2)
        self.comboBox_jointSelection.setObjectName(u"comboBox_jointSelection")

        self.horizontalLayout_3.addWidget(self.comboBox_jointSelection)


        self.verticalLayout_4.addWidget(self.frame_2)

        self.tabWidget.addTab(self.tab_positions, "")
        self.tab_hands = QWidget()
        self.tab_hands.setObjectName(u"tab_hands")
        self.horizontalLayout = QHBoxLayout(self.tab_hands)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(self.tab_hands)
        self.frame.setObjectName(u"frame")
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.groupBox_xLandmarks = QGroupBox(self.frame)
        self.groupBox_xLandmarks.setObjectName(u"groupBox_xLandmarks")
        self.gridLayout_3 = QGridLayout(self.groupBox_xLandmarks)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_left = QLabel(self.groupBox_xLandmarks)
        self.label_left.setObjectName(u"label_left")

        self.gridLayout_3.addWidget(self.label_left, 3, 1, 1, 1)

        self.label_middle = QLabel(self.groupBox_xLandmarks)
        self.label_middle.setObjectName(u"label_middle")

        self.gridLayout_3.addWidget(self.label_middle, 2, 1, 1, 1)

        self.pushButton_middle = QPushButton(self.groupBox_xLandmarks)
        self.pushButton_middle.setObjectName(u"pushButton_middle")

        self.gridLayout_3.addWidget(self.pushButton_middle, 2, 0, 1, 1)

        self.pushButton_left = QPushButton(self.groupBox_xLandmarks)
        self.pushButton_left.setObjectName(u"pushButton_left")

        self.gridLayout_3.addWidget(self.pushButton_left, 3, 0, 1, 1)

        self.pushButton_right = QPushButton(self.groupBox_xLandmarks)
        self.pushButton_right.setObjectName(u"pushButton_right")

        self.gridLayout_3.addWidget(self.pushButton_right, 0, 0, 1, 1)

        self.label_right = QLabel(self.groupBox_xLandmarks)
        self.label_right.setObjectName(u"label_right")

        self.gridLayout_3.addWidget(self.label_right, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_xLandmarks, 1, 0, 1, 2)

        self.groupBox_yLandmarks = QGroupBox(self.frame)
        self.groupBox_yLandmarks.setObjectName(u"groupBox_yLandmarks")
        self.gridLayout_2 = QGridLayout(self.groupBox_yLandmarks)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton = QPushButton(self.groupBox_yLandmarks)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.groupBox_yLandmarks)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_2.addWidget(self.pushButton_3, 2, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.groupBox_yLandmarks)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_2.addWidget(self.pushButton_2, 0, 0, 1, 1)

        self.label_up = QLabel(self.groupBox_yLandmarks)
        self.label_up.setObjectName(u"label_up")

        self.gridLayout_2.addWidget(self.label_up, 0, 1, 1, 1)

        self.label_center = QLabel(self.groupBox_yLandmarks)
        self.label_center.setObjectName(u"label_center")

        self.gridLayout_2.addWidget(self.label_center, 1, 1, 1, 1)

        self.label_down = QLabel(self.groupBox_yLandmarks)
        self.label_down.setObjectName(u"label_down")

        self.gridLayout_2.addWidget(self.label_down, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_yLandmarks, 4, 0, 1, 2)

        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBox_face = QCheckBox(self.groupBox_2)
        self.checkBox_face.setObjectName(u"checkBox_face")
        self.checkBox_face.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox_face)

        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_rightHand = QCheckBox(self.groupBox_3)
        self.checkBox_rightHand.setObjectName(u"checkBox_rightHand")
        self.checkBox_rightHand.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_rightHand)

        self.checkBox_leftHand = QCheckBox(self.groupBox_3)
        self.checkBox_leftHand.setObjectName(u"checkBox_leftHand")
        self.checkBox_leftHand.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_leftHand)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.checkBox_body = QCheckBox(self.groupBox_2)
        self.checkBox_body.setObjectName(u"checkBox_body")
        self.checkBox_body.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox_body)


        self.gridLayout.addWidget(self.groupBox_2, 5, 0, 1, 2)

        self.pushButton_play = QPushButton(self.frame)
        self.pushButton_play.setObjectName(u"pushButton_play")
        sizePolicy2.setHeightForWidth(self.pushButton_play.sizePolicy().hasHeightForWidth())
        self.pushButton_play.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pushButton_play, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 0, 1, 2)


        self.horizontalLayout.addWidget(self.frame)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.tabWidget.addTab(self.tab_hands, "")

        self.horizontalLayout_4.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_cameraView.setText(QCoreApplication.translate("Form", u"Camera View", None))
        self.label.setText(QCoreApplication.translate("Form", u"Joint", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_positions), QCoreApplication.translate("Form", u"Positions", None))
        self.groupBox_xLandmarks.setTitle(QCoreApplication.translate("Form", u"X Landmarks", None))
        self.label_left.setText(QCoreApplication.translate("Form", u"Position", None))
        self.label_middle.setText(QCoreApplication.translate("Form", u"Position", None))
        self.pushButton_middle.setText(QCoreApplication.translate("Form", u"Define Middle Line", None))
        self.pushButton_left.setText(QCoreApplication.translate("Form", u"Define Left Line", None))
        self.pushButton_right.setText(QCoreApplication.translate("Form", u"Define Right Line", None))
        self.label_right.setText(QCoreApplication.translate("Form", u"Position", None))
        self.groupBox_yLandmarks.setTitle(QCoreApplication.translate("Form", u"Y Landmarks", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Define Center", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Define Down", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"Define Up", None))
        self.label_up.setText(QCoreApplication.translate("Form", u"Position", None))
        self.label_center.setText(QCoreApplication.translate("Form", u"Position", None))
        self.label_down.setText(QCoreApplication.translate("Form", u"Position", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Show Tracking Points", None))
        self.checkBox_face.setText(QCoreApplication.translate("Form", u"Face", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Hands", None))
        self.checkBox_rightHand.setText(QCoreApplication.translate("Form", u"Right", None))
        self.checkBox_leftHand.setText(QCoreApplication.translate("Form", u"Left", None))
        self.checkBox_body.setText(QCoreApplication.translate("Form", u"Body", None))
        self.pushButton_play.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_hands), QCoreApplication.translate("Form", u"Settings", None))
    # retranslateUi

