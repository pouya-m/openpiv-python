
import PIV
from openpiv import tools, validation, filters
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
        self.setWindowTitle('PIV - Build 0.2')
        self.resize(1280, 800)
        self.file_list = {}
        self.first_plot = True
        self.actionload_files.triggered.connect(self.select_files)
        self.actionexit.triggered.connect(qApp.quit)
        self.apply_settings_PB.clicked.connect(lambda: self.update_list(setchange=1))
        self.load_settings_PB.clicked.connect(self.load_settings)
        self.save_settings_PB.clicked.connect(self.save_settings)
        selmodel = self.files_TW.selectionModel()
        selmodel.currentChanged.connect(self.update_plot)
        self.plot_settings_LE.editingFinished.connect(self.update_plot_settings)
        self.BV_settings_CB.currentTextChanged.connect(self.update_plot_settings)
        self.update_plot_settings()

        # Create the maptlotlib FigureCanvas object
        self.valplot = MplCanvas(self, width=5, height=4, dpi=100)
        self.valplot.axes.set_autoscale_on(False)
        self.valplot.axes.text(5, 5, 'Add files to analze using the menubar... \n Then select a file from the list to plot', \
            ha='center', va='center',style='italic', size=12)
        self.valplot.axes.axis([0, 10, 0, 10])
        # Create toolbar, passing canvas as first parament
        toolbar = NavigationToolbar(self.valplot, self)
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(toolbar)
        layout1.addWidget(self.plot_settings_LE)
        layout1.addWidget(self.BV_settings_CB)
        layout2 = QtWidgets.QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(self.valplot)
        # use plot_widget to hold our toolbar and canvas.
        self.plot_widget.setLayout(layout2)

        self.show()

    def select_files(self):
        file_paths, ext = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files')
        self.update_list(file_paths=file_paths)
    

    def update_list(self, file_paths=None, setchange=None):
        t1 = time.time()
        if self.files_TW.currentItem():
            current_key = self.files_TW.currentItem().text(0)
        else:
            current_key = None
        self.files_TW.clear()
        if setchange is None:
            for path in file_paths:
                *_, u, v, sig2noise = tools.read_data(path)
                key = os.path.basename(path)
                mask_temp = np.zeros(u.shape, dtype=bool)
                self.file_list[key] = [path, mask_temp, u, v, sig2noise]
                self.file_list[key][1] = self.calc_mask(key=key)
        else:
            for key in self.file_list.keys():
                self.file_list[key][1] = self.calc_mask(key=key)
        for key in self.file_list.keys():
            item = QtWidgets.QTreeWidgetItem(self.files_TW) 
            item.setText(0, key)
            item.setText(1, str(int(np.sum(self.file_list[key][1]))))
            if key == current_key:
                self.files_TW.setCurrentItem(item)
        dt = time.time()-t1
        print(f'processing done in {dt:.2f} sec')

    def calc_mask(self, key):
        u1, v1 = self.file_list[key][2], self.file_list[key][3]
        u, v = u1.copy(), v1.copy()
        if self.s2n_CB.isChecked():
            sig2noise = self.file_list[key][4]
            thr = float(self.s2n_LE.text())
            u, v, mask1 = validation.sig2noise_val( u, v, sig2noise, threshold = thr )
        else:
            mask1 = np.zeros(u.shape, dtype=bool)
        if self.global_velocity_CB.isChecked():
            ulim = [float(i) for i in self.global_uVelocity_LE.text().split(',')]
            vlim = [float(i) for i in self.global_vVelocity_LE.text().split(',')]
            u, v, mask2 = validation.global_val( u, v, (ulim[0], ulim[1]), (vlim[0], vlim[1]) )
        else:
            mask2 = np.zeros(u.shape, dtype=bool)
        if self.local_velocity_CB.isChecked():
            lim = [float(i) for i in self.local_velocity_LE.text().split(',')]
            ksize = int(self.local_kernel_LE.text())
            u, v, mask3 = validation.local_median_val(u, v, lim[0], lim[1], size=ksize)
        else:
            mask3 = np.zeros(u.shape, dtype=bool)
        if self.global_std_CB.isChecked():
            std = float(self.global_std_LE.text())
            u, v, mask4 = validation.global_std(u, v, std_threshold=std)
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
            if self.first_plot is False:
                xmin, xmax = self.valplot.axes.get_xlim()
                ymin, ymax = self.valplot.axes.get_ylim()
            else:
                xmin, xmax, ymin, ymax = None, None, None, None
                self.first_plot = False

            self.valplot.axes.cla()
            if (self.BV_settings == 'Show Original BV') or (self.BV_settings == 'Only Show BV'):
                self.valplot.axes.quiver(x[mask], y[mask], u[mask], v[mask], color=self.invalid_col, \
                    units='xy', scale=float(self.scale), width=float(self.width), minlength=0.1, minshaft=1.2)
            elif self.BV_settings == 'Show Replaced BV':
                u[mask], v[mask] = np.nan, np.nan
                u, v = filters.replace_outliers( u, v, method='localmean', max_iter=10, kernel_size=2)
                self.valplot.axes.quiver(x[mask], y[mask], u[mask], v[mask], color=self.invalid_col, \
                    units='xy', scale=float(self.scale), width=float(self.width), minlength=0.1, minshaft=1.2)
            elif self.BV_settings == 'Do Not Show BV':
                pass
            if self.BV_settings != 'Only Show BV':
                self.valplot.axes.quiver(x[valid], y[valid], u[valid], v[valid], color=self.valid_col, \
                    units='xy', scale=float(self.scale), width=float(self.width), minlength=0.1, minshaft=1.2)

            self.valplot.axes.set_xlim(xmin, xmax)
            self.valplot.axes.set_ylim(ymin, ymax)
            self.valplot.draw()
            dt = time.time()-t1
            print(f'drawing done in {dt:.2f} sec')
    
    def update_plot_settings(self):
        self.BV_settings = self.BV_settings_CB.currentText()
        self.valid_col, self.invalid_col, self.scale, self.width = self.plot_settings_LE.text().split(',')
        self.update_plot(self.files_TW.currentIndex())

    
    def save_settings(self):
        #getting the settings
        s2n_state = str(self.s2n_CB.isChecked())
        s2n_LE = self.s2n_LE.text()
        gv_state = str(self.global_velocity_CB.isChecked())
        gv_LE1 = self.global_uVelocity_LE.text()
        gv_LE2 = self.global_vVelocity_LE.text()
        lv_state = str(self.local_velocity_CB.isChecked())
        lv_LE1 = self.local_velocity_LE.text()
        lv_LE2 = self.local_kernel_LE.text()
        gs_state = str(self.global_std_CB.isChecked())
        gs_LE = self.global_std_LE.text()
        #getting the file path
        path, ext = QtWidgets.QFileDialog.getSaveFileName(self, \
            'Select a location to save the settings', 'Validation_Settings.dat')
        #saving to file
        with open(path, 'w') as fh:
            fh.write('Validation settings:\n')
            fh.write(s2n_state+';'+s2n_LE+'\n')
            fh.write(gv_state+';'+gv_LE1+';'+gv_LE2+'\n')
            fh.write(lv_state+';'+lv_LE1+';'+lv_LE2+'\n')
            fh.write(gs_state+';'+gs_LE+'\n')  

    def load_settings(self):
        #load and read file
        path, ext = QtWidgets.QFileDialog.getOpenFileName(self, \
            'Select settings file', 'Validation_Settings.dat')
        lines = []
        with open(path, 'r') as fh:
            for line in fh:
                lines.append(line[:-1])
        #extract and set values
        s2n_state, s2n_LE = lines[1].split(';')
        gv_state, gv_LE1, gv_LE2 = lines[2].split(';')
        lv_state, lv_LE1, lv_LE2 = lines[3].split(';')
        gs_state, gs_LE = lines[4].split(';')
        self.s2n_CB.setChecked(eval(s2n_state))
        self.s2n_LE.setText(s2n_LE)
        self.global_velocity_CB.setChecked(eval(gv_state))
        self.global_uVelocity_LE.setText(gv_LE1)
        self.global_vVelocity_LE.setText(gv_LE2)
        self.local_velocity_CB.setChecked(eval(lv_state))
        self.local_velocity_LE.setText(lv_LE1)
        self.local_kernel_LE.setText(lv_LE2)
        self.global_std_CB.setChecked(eval(gs_state))
        self.global_std_LE.setText(gs_LE)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qt_app = Myapp()
    app.exec_()

