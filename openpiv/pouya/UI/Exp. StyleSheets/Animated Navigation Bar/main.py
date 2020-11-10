# Example menu toggle animation
# Adampted from Wanderson's youtube video: https://www.youtube.com/watch?v=5u2805f0xFw&list=PLfQ7GQSrl0_t0hkgOk_Wxdjx9v2vjKfu9&index=7


import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# Import GUI file and functions
from ui_main import Ui_MainWindow
from ui_functions import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## Toggle menu
        self.ui.frame_left_menu.enterEvent = lambda event: UIFunctions.toggleMenu(self, 150)
        self.ui.frame_left_menu.leaveEvent = lambda event: UIFunctions.toggleMenu(self, 70)

        ## Pages
        self.ui.btn_page_1.clicked.connect(lambda: self.btnClicked(1))
        self.ui.btn_page_2.clicked.connect(lambda: self.btnClicked(2))
        self.ui.btn_page_3.clicked.connect(lambda: self.btnClicked(3))

        self.show()

    def btnClicked(self, btn):
        if btn == 1:
            self.ui.btn_page_2.setChecked(False)
            self.ui.btn_page_3.setChecked(False)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)
        elif btn == 2:
            self.ui.btn_page_1.setChecked(False)
            self.ui.btn_page_3.setChecked(False)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        else:
            self.ui.btn_page_1.setChecked(False)
            self.ui.btn_page_2.setChecked(False)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
