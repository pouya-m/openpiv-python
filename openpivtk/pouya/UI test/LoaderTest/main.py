# this example program shows how to load a .ui file directly and use it in the application main window.
# the QUiLoader from PySide returns a QWidget object that can be set as the central widget of a main window! 
# it can't be the main window itself. then the returned widget needs to be save (here as self.ui) and then its' 
# children can be accessed from self (here self.ui)


from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QAction
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
import os, sys


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.loadMainWidget()
        self.addMenuBar()
        self.setWindowTitle(f'Test GUI - V0.1')
        self.resize(400,250)
        self.ui.PB1.clicked.connect(lambda : print('PB1 clicked'))
        self.ui.PB2.clicked.connect(lambda : print('PB2 clicked'))
        

    def loadMainWidget(self):
        loader = QUiLoader()
        ui_file = QFile(os.path.join(os.path.dirname(__file__), "main.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def addMenuBar(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        helpmenu = menubar.addMenu('Help')
        openAction = QAction('Open', self)
        deleteAction = QAction('Delete Selection', self)
        clearAction = QAction('Clear', self)
        exitAction = QAction('Exit', self)
        aboutAction = QAction('About', self)
        openAction.setShortcut('Ctrl+O')
        deleteAction.setShortcut('Delete')
        filemenu.addAction(openAction)
        filemenu.addAction(deleteAction)
        filemenu.addAction(clearAction)
        filemenu.addAction(exitAction)
        helpmenu.addAction(aboutAction)
        #openAction.triggered.connect(self.openFiles)
        #deleteAction.triggered.connect(self.deleteSelection)
        #clearAction.triggered.connect(self.listWidget.clear)
        exitAction.triggered.connect(QApplication.quit)
        #aboutAction.triggered.connect(self.showAbout)  

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec_())