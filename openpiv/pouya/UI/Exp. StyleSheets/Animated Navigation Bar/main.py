# Example menu toggle animation
# Adampted from Wanderson's youtube video: https://www.youtube.com/watch?v=5u2805f0xFw&list=PLfQ7GQSrl0_t0hkgOk_Wxdjx9v2vjKfu9&index=7


import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# Import GUI file
from ui_main import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        ## Toggle menu
        self.frame_left_menu.enterEvent = lambda event: self.toggleMenu(150)
        self.frame_left_menu.leaveEvent = lambda event: self.toggleMenu(50)

        ## Pages
        self.btn_page_1.clicked.connect(lambda: self.btnClicked(1))
        self.btn_page_2.clicked.connect(lambda: self.btnClicked(2))
        self.btn_page_3.clicked.connect(lambda: self.btnClicked(3))

        self.show()

    def btnClicked(self, btn):
        if btn == 1:
            self.btn_page_2.setChecked(False)
            self.btn_page_3.setChecked(False)
            self.stackedWidget.setCurrentWidget(self.page_1)
        elif btn == 2:
            self.btn_page_1.setChecked(False)
            self.btn_page_3.setChecked(False)
            self.stackedWidget.setCurrentWidget(self.page_2)
        else:
            self.btn_page_1.setChecked(False)
            self.btn_page_2.setChecked(False)
            self.stackedWidget.setCurrentWidget(self.page_3)
            
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
