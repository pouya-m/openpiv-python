from PySide2 import QtWidgets
from PySide2.QtGui import QPixmap, Qt, QIcon, QKeySequence
from PySide2.QtCore import QTimer
#import qdarkstyle
import ImageOpener

import matplotlib
#matplotlib.rcParams['figure.facecolor'] = '#19232D'
#matplotlib.rcParams['axes.facecolor'] = '#19232D'
#matplotlib.rc_context({'axes.edgecolor':'xkcd:grey', 'xtick.color':'xkcd:grey', 'ytick.color':'xkcd:grey'})
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from imageio import imread
import os, time, sys

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Window(ImageOpener.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Image Viewer - Build 001')
        self.setWindowIcon(QIcon("C:\\Users\\Asus\\Desktop\\UI\\ImageOpener\\viewerIcon.png"))
        self.show()
        self.actionOpen.triggered.connect(self.selectFiles)
        self.actionExit.triggered.connect(qApp.exit)
        self.nextPB.clicked.connect(self.nextImage)
        self.previousPB.clicked.connect(self.previousImage)
        # creating key shortcuts
        self.nextShortcut = QtWidgets.QShortcut(QKeySequence('Right'), self)
        self.previousShortcut = QtWidgets.QShortcut(QKeySequence('Left'), self)
        self.nextShortcut.activated.connect(self.nextImage)
        self.previousShortcut.activated.connect(self.previousImage)
        # Create the maptlotlib FigureCanvas object
        self.valplot = MplCanvas(self, width=5, height=4, dpi=100)
        self.valplot.axes.text(5, 5, 'Open images to show from: Files->Open', \
            ha='center', va='center',style='italic', size=14)
        self.valplot.axes.axis([0, 10, 0, 10])
        # Create toolbar, passing canvas as first parent and add to layout
        toolbar = NavigationToolbar(self.valplot, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.valplot)
        self.frame.setLayout(layout)
        self.files = []
        self.fileN = 0

    def selectFiles(self):
        file_paths, ext = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files')
        if file_paths != []:
            self.files = file_paths
            self.fileN = 0
            self.valplot.axes.clear()
            self.viewImage(self.files[0], reset=True)

    def viewImage(self, file, reset=False):
        Img = imread(file)
        xmin, xmax = self.valplot.axes.get_xlim()
        ymin, ymax = self.valplot.axes.get_ylim()
        self.valplot.axes.cla()
        self.valplot.axes.imshow(Img, cmap='gray', vmin=0, vmax=1000)
        if reset is False:
            self.valplot.axes.set_xlim(xmin, xmax)
            self.valplot.axes.set_ylim(ymin, ymax)
        self.valplot.draw()
        self.label.setText(os.path.basename(file))

    def nextImage(self):
        if self.fileN < (len(self.files) - 1):
            self.fileN = self.fileN + 1
            self.viewImage(self.files[self.fileN])

    def previousImage(self):
        if self.fileN > 0:
            self.fileN = self.fileN - 1
            self.viewImage(self.files[self.fileN])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    pixmap = QPixmap("SplashFrog.jpg")
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
    splash.show()
    QTimer.singleShot(3000, splash.close)
    window = Window()
    sys.exit(app.exec_())

