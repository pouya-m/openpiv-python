from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QAbstractItemView
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon
import sys, os, time
import tecplot as tp
from tecplot.constant import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.version = 0.2
        self.setWindowTitle(f'File Walker Tool - V{self.version}')
        self.resize(450,600)
        dirname = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(os.path.join(dirname, 'walker.ico')))
        self.setStyleSheet(open(os.path.join(dirname, 'darkorange.qss'),'r').read())
        self.setAcceptDrops(True)
        self.mainwidget = QtWidgets.QWidget()
        self.mainwidget.setAcceptDrops(True)
        self.setCentralWidget(self.mainwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainwidget)
        self.listWidget = QtWidgets.QListWidget()
        self.verticalLayout.addWidget(self.listWidget)
        self.addMenuBar()
        #tp.session.connect()
        self.listWidget.currentTextChanged.connect(self.sendTecplotCommand)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setDragEnabled(True)
        self.listWidget.viewport().setAcceptDrops(True)
        self.listWidget.setDropIndicatorShown(True)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.tecplotReady = True
        #self.textBox = tp.active_frame().add_text('', position=(40,90))
            
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            file_paths = []
            for url in event.mimeData().urls():
                file_paths.append(str(url.toLocalFile()))
            self.listWidget.addItems(file_paths)
        else:
            event.ignore()
        
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
        openAction.triggered.connect(self.openFiles)
        deleteAction.triggered.connect(self.deleteSelection)
        clearAction.triggered.connect(self.listWidget.clear)
        exitAction.triggered.connect(QApplication.quit)
        aboutAction.triggered.connect(self.showAbout)       
    
    def openFiles(self):
        file_paths, ext = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files to walk through')
        self.listWidget.addItems(file_paths)

    def sendTecplotCommand(self, current):
        if os.path.isfile(current) and self.tecplotReady:
            self.tecplotReady = False
            self.update_tecplot = UpdateTecplot(current, self.textBox)
            self.update_tecplot.start()

    def deleteSelection(self):
        selected = self.listWidget.selectedItems()
        for item in selected:
            self.listWidget.takeItem(self.listWidget.row(item))

    def showAbout(self):
        QtWidgets.QMessageBox.information(self, 'About', f'File Walker Tool for Tecplot\nVersion {self.version}\nSimple program to walk through files and easily view them without changing Tecplot settings. Can also be integrated into Tecplot as a quick macro!\nBy Pouya Mohtat')


class UpdateTecplot(QtCore.QThread):

    def __init__(self, current, textBox):
        super(UpdateTecplot, self).__init__()
        self.current = current
        self.textBox = textBox

    def run(self):
        tp.data.load_tecplot(self.current, 
            read_data_option=ReadDataOption.ReplaceInActiveFrame,
            reset_style=False)
        self.textBox.text_string = os.path.basename(self.current)
        print(f'opened: {self.current}')
        window.tecplotReady = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())
