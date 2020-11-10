################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

## ==> GUI FILE
#from main import *
from PySide2 import QtCore, QtGui, QtWidgets



#class UIFunctions(MainWindow):
def toggleMenu(self, maxWidth, enable):
    if enable:

        # GET WIDTH
        width = self.width()
        maxExtend = maxWidth
        standard = 70

        # SET MAX WIDTH
        if width == 70:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QtCore.QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

class LeftBar(QtWidgets.QFrame):

    def enterEvent(self, event):
        toggleMenu(self, 250, True)

    def leaveEvent(self, event):
        toggleMenu(self, 250, True)