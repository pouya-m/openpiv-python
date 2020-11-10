from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QAbstractItemView
from PySide2 import QtWidgets, QtCore
import sys, os
import tecplot as tp
from tecplot.constant import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Walker Tool - V0.1")
        self.resize(450,600)
        self.setAcceptDrops(True)
        self.mainwidget = QtWidgets.QWidget()
        self.mainwidget.setAcceptDrops(True)
        self.setCentralWidget(self.mainwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainwidget)
        self.listWidget = QtWidgets.QListWidget()
        self.verticalLayout.addWidget(self.listWidget)
        self.addMenuBar()
        tp.session.connect()
        self.listWidget.currentTextChanged.connect(self.updateTecplot)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.setDragEnabled(True)
        self.listWidget.viewport().setAcceptDrops(True)
        self.listWidget.setDropIndicatorShown(True)
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)

            
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
        openAction = QAction('Open', self)
        deleteAction = QAction('Delete Selection', self)
        clearAction = QAction('Clear', self)
        exitAction = QAction('Exit', self)
        openAction.setShortcut('Ctrl+O')
        deleteAction.setShortcut('Delete')
        filemenu.addAction(openAction)
        filemenu.addAction(deleteAction)
        filemenu.addAction(clearAction)
        filemenu.addAction(exitAction)
        openAction.triggered.connect(self.openFiles)
        deleteAction.triggered.connect(self.deleteSelection)
        clearAction.triggered.connect(self.listWidget.clear)
        exitAction.triggered.connect(QApplication.quit)       
    
    def openFiles(self):
        file_paths, ext = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files to walk through')
        self.listWidget.addItems(file_paths)

    def updateTecplot(self, current):
        if os.path.isfile(current):
            tp.data.load_tecplot(current, 
                read_data_option=ReadDataOption.ReplaceInActiveFrame,
                reset_style=False)
            print(f'opened: {current}')

    def deleteSelection(self):
        selected = self.listWidget.selectedItems()
        #if selected is []:
        #    return
        for item in selected:
            self.listWidget.takeItem(self.listWidget.row(item))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())
