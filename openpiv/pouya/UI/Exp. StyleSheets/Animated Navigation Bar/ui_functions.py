
from main import *

class UIFunctions(MainWindow):

    def toggleMenu(self, width):
        # Get width
        last_width = self.ui.frame_left_menu.width()
        
        # Animation
        self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(last_width)
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
        

