# author: Michael Hüppe
# date: 09.04.2024
# project: bodyTracking/movement_detection.py
import sys

import numpy as np
from PySide2.QtGui import QPalette, QColor, Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from .gui.tabWidget import BodyTrackingWidget
from .resources.bodyTracker import BodyTracker
class BodyTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Body Tracking")

        # Create instance for gui
        self.mainView = BodyTrackingWidget(
            cb_updateTrackingVisibility=self._gui_updateBodyTrackingVisibility,
            cb_updateJoint=self._gui_updateJoint
        )
        # Create instance for body tracking
        # cam_input = r"C:\Users\mhuep\Master_Informatik\Semester_2\InteractiveGameDesign\bodytracking\sample_video.mov"
        cam_input = 0
        self._bodyTracker = BodyTracker(cb_sendBodyImage=self._bodyTracker_sendBodyImage,
                                        cb_sendBodyPositions=self._bodyTracker_sendBodyPositions,
                                        cameraIndex=cam_input)
        # Set custom widget as central widget
        self.setCentralWidget(self.mainView)
        self.mainView.handle_toggleWebcam(True)

    # Gui Event handling
    def _gui_updateBodyTrackingVisibility(self, settings: dict):
        """
        Update the visibility in the plot
        :param settings: which parts should be shown and which not
        :return:
        """
        self._bodyTracker.setTrackingVisibility(settings)

    def _gui_updateJoint(self, name: str, jointIndex: int):
        """
        Update the joint for the view and which joint to send
        :param name: Specification of the joint
        :param jointIndex: Index of the joint
        """
        self._bodyTracker.setJoint(jointIndex)
        self.mainView.setName(name)
    # body Tracking handling
    def _bodyTracker_sendBodyImage(self, image: np.ndarray):
        """
        Send the body image to the main View
        :param image: Image of the body with the poses drawn onto
        :return:
        """
        self.mainView.setImage(image)

    def _bodyTracker_sendBodyPositions(self, positions: np.ndarray):
        """
        Distribute the positions of the body
        :param positions:
        :return:
        """
        self.mainView.updatePosition(positions)
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(55, 55, 55))
    palette.setColor(QPalette.Disabled, QPalette.Button, QColor(20, 20, 20))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    # Create and show the main window
    window = BodyTrackerWindow()
    window.setGeometry(100, 100, 400, 300)  # Set window position and size
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
