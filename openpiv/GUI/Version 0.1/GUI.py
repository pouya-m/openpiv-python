
import PIV
from openpiv import tools, validation
import numpy as np
import os
from PySide2 import QtWidgets
import time

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Myapp(PIV.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Myapp, self).__init__()
        self.setupUi(self)
        #self.showMaximized()
        self.setWindowTitle('PIV - Build 0.1')
        self.file_list = {}
        self.actionload_files.triggered.connect(self.select_files)
        self.actionexit.triggered.connect(qApp.quit)
        self.apply_settings_PB.clicked.connect(lambda: self.update_list(setchange=1))
        self.load_settings_PB.clicked.connect(self.load_settings)
        self.save_settings_PB.clicked.connect(self.save_settings)
        selmodel = self.files_TW.selectionModel()
        selmodel.currentChanged.connect(self.update_plot)

        # Create the maptlotlib FigureCanvas object
        self.valplot = MplCanvas(self, width=5, height=4, dpi=100)
        self.valplot.axes.text(5, 5, 'Add files to analze using the menubar... \n Then select a file from the list to plot', \
            ha='center', va='center',style='italic', size=12)
        self.valplot.axes.axis([0, 10, 0, 10])
        # Create toolbar, passing canvas as first parament
        toolbar = NavigationToolbar(self.valplot, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.valplot)
        # use plot_widget to hold our toolbar and canvas.
        self.plot_widget.setLayout(layout)

        self.show()

    def select_files(self):
        file_paths, ext = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files')
        self.update_list(file_paths=file_paths)
    

    def update_list(self, file_paths=None, setchange=None):
        t1 = time.time()
        self.files_TW.clear()
        if setchange is None:
            for path in file_paths:
                *_, u, v, sig2noise = tools.read_data(path)
                key = os.path.basename(path)
                self.file_list[key] = [path, 0, u, v, sig2noise]
                self.file_list[key][1] = self.calc_mask(key=key)
        else:
            for key in self.file_list.keys():
                self.file_list[key][1] = self.calc_mask(key=key)
        for key in self.file_list.keys():
            item = QtWidgets.QTreeWidgetItem(self.files_TW) 
            item.setText(0, key)
            item.setText(1, str(int(np.sum(self.file_list[key][1]))))
        dt = time.time()-t1
        print(f'processing done in {dt:.2f} sec')
        self.update_plot(self.files_TW.currentIndex())

    def calc_mask(self, key):
        u, v = self.file_list[key][2], self.file_list[key][3]
        if self.s2n_CB.isChecked():
            sig2noise = self.file_list[key][4]
            thr = float(self.s2n_LE.text())
            *_, mask1 = validation.sig2noise_val( u, v, sig2noise, threshold = thr )
        else:
            mask1 = np.zeros(u.shape, dtype=bool)
        if self.global_velocity_CB.isChecked():
            ulim = [float(i) for i in self.global_uVelocity_LE.text().split(',')]
            vlim = [float(i) for i in self.global_vVelocity_LE.text().split(',')]
            *_, mask2 = validation.global_val( u, v, (ulim[0], ulim[1]), (vlim[0], vlim[1]) )
        else:
            mask2 = np.zeros(u.shape, dtype=bool)
        if self.local_velocity_CB.isChecked():
            lim = [float(i) for i in self.local_velocity_LE.text().split(',')]
            ksize = int(self.local_kernel_LE.text())
            *_, mask3 = validation.local_median_val(u, v, lim[0], lim[1], size=ksize)
        else:
            mask3 = np.zeros(u.shape, dtype=bool)
        if self.global_std_CB.isChecked():
            std = float(self.global_std_LE.text())
            *_, mask4 = validation.global_std(u, v, std_threshold=std)
        else:
            mask4 = np.zeros(u.shape, dtype=bool)

        mask = mask1 | mask2 | mask3 | mask4
        
        return mask

    def update_plot(self, current, previous=None):
        if self.files_TW.itemFromIndex(current):
            t1 = time.time()
            key = self.files_TW.itemFromIndex(current).text(0)
            x, y, u, v, *_ = tools.read_data(self.file_list[key][0])
            mask = self.file_list[key][1]
            valid = ~mask
            self.valplot.axes.cla()
            self.valplot.axes.quiver(x[mask], y[mask], u[mask], v[mask], color='r', scale=None, width=0.0035)
            self.valplot.axes.quiver(x[valid], y[valid], u[valid], v[valid], color='b', scale=None, width=0.0035)
            self.valplot.draw()
            dt = time.time()-t1
            print(f'drawing done in {dt:.2f} sec')
    
    def save_settings(self):
        s2n_state = self.s2n_CB.isChecked()
        s2n_LE_val = self.s2n_LE.text()
        save_path, ext = QtWidgets.QFileDialog.getSaveFileName(self, \
            'Select a location to save the settings', 'Validation_Settings.dat')
        
        print(save_path)

    def load_settings(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qt_app = Myapp()
    app.exec_()

