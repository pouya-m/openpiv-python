# Example menu toggle animation
# Adampted from Wanderson's youtube video: https://www.youtube.com/watch?v=5u2805f0xFw&list=PLfQ7GQSrl0_t0hkgOk_Wxdjx9v2vjKfu9&index=7


import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# Import GUI file
from ui_main import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # toggle menu
        self.frame_left_menu.enterEvent = lambda event: self.toggleMenu(180)
        self.frame_left_menu.leaveEvent = lambda event: self.toggleMenu(90)

        # main tabs
        self.current_main_PB = self.freq_analysis_PB
        self.validation_PB.clicked.connect(lambda: self.mainTabClicked(self.validation_PB, self.validation_tab))
        self.processing_PB.clicked.connect(lambda: self.mainTabClicked(self.processing_PB, self.processing_tab))
        self.freq_analysis_PB.clicked.connect(lambda: self.mainTabClicked(self.freq_analysis_PB, self.frequency_tab))
        self.modal_analysis_PB.clicked.connect(lambda: self.mainTabClicked(self.modal_analysis_PB, self.modal_tab))
        # process tabs
        self.current_process_FR = self.experiment_frame
        self.current_process_PB = self.experiment_PB
        self.experiment_PB.clicked.connect(lambda: self.processTabClicked(self.experiment_PB, self.experiment_frame))
        self.preprocess_PB.clicked.connect(lambda: self.processTabClicked(self.preprocess_PB, self.preprocess_frame))
        self.process_PB.clicked.connect(lambda: self.processTabClicked(self.process_PB, self.process_frame))
        self.postprocess_PB.clicked.connect(lambda: self.processTabClicked(self.postprocess_PB, self.postprocess_frame))


        self.show()

    def processTabClicked(self, PB, FR):
        H = self.current_process_FR.height()
        # set up the animations
        self.tab_anim1 = QPropertyAnimation(FR, b"maximumHeight")
        self.tab_anim1.setDuration(400)
        self.tab_anim1.setStartValue(20)
        self.tab_anim1.setEndValue(H)
        self.tab_anim1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.tab_anim2 = QPropertyAnimation(self.current_process_FR, b"maximumHeight")
        self.tab_anim2.setDuration(400)
        self.tab_anim2.setStartValue(H)
        self.tab_anim2.setEndValue(20)
        self.tab_anim2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.tab_anim1)
        self.anim_group.addAnimation(self.tab_anim2)
        self.anim_group.start()
        # set last button and frame
        PB.setEnabled(False)
        self.current_process_FR = FR
        self.current_process_PB.setEnabled(True)
        self.current_process_PB = PB
            

    def mainTabClicked(self, PB, tab):
        self.main_tabs.setCurrentWidget(tab)
        PB.setChecked(True)
        self.current_main_PB.setChecked(False)
        self.current_main_PB = PB
            

    def toggleMenu(self, width):
        # Get width
        last_width = self.frame_left_menu.width()
        
        # Animation
        self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(last_width)
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
