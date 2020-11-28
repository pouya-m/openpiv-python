# Particle Image Velocimetry GUI
# By Pouya Mohtat Nov. 2020

# Version 0.6 change log:
# - Modal analysis tab now active
# - the filters are uncoupled (u and v are not changed in validation and only the mask is calculated and returned)
# - the experiment folder addressing is changed and patterns are used instead of single folder names, making the folder addresses more flexible.
# - code to find background image is vectorized and operates more efficiently and much faster. Also the GUI automatically searches for background files.
#   if there are in the analysis folder then it uses the existing bg files otherwise it calculates the bg.
# - 'import raw images' dialogue is removed all together. the same functionality can be achieved using the process tab and then import unvalidated files.

# to do:
#------------------------------------
# 1- local median filter seems to work better with kernal=2 but in some situations it will not catch bad vectors with kernel=2 and we need to specify kernel=1 to catch them.
#    this should be investigated and possibly we should provide an option to apply multiple median filters back to back or with vector replacement in between. 

# 2- stop buttons don't do anything at the moment. they should provide a gracefull exit from the current running process.
#    it's necessary to have a stop flag to properly exit from the main 'task.run' multiprocessing loop and have all the child processes 
#    and workers neatly closed and the resources freed up.


from PySide2 import QtWidgets
from PySide2.QtCore import QThread, Signal, QTimer, Qt
from PySide2.QtGui import QIcon
import Main_PIV
from openpiv import tools, validation, filters, pyprocess, scaling, smoothn, postprocessing, modal
import numpy as np
import os, sys, glob
from functools import partial
import multiprocessing
from imageio import imsave
import styles

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainPIV(Main_PIV.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(MainPIV, self).__init__()
        self.setupUi(self)

        #self.showMaximized()
        self.version = 0.6
        self.setWindowTitle(f'PIV Analysis Toolkit V{self.version}')
        self.resize(1280, 800)
        self.show()
        self.file_list = {}
        self.first_plot = True
        self.actionLoad_Files.triggered.connect(self.selectFiles)
        self.run_progress_TE.ensureCursorVisible()
        self.actionExit.triggered.connect(qApp.quit)
        self.actionClear_Files.triggered.connect(self.clearList)
        self.actionAbout.triggered.connect(self.showAbout)
        self.apply_settings_PB.clicked.connect(lambda: self.updateList(setchange=1))
        self.load_settings_PB.clicked.connect(self.loadThrSettings)
        self.save_settings_PB.clicked.connect(self.saveThrSettings)
        selmodel = self.files_TW.selectionModel()
        selmodel.currentChanged.connect(self.updatePlot)
        self.plot_settings_LE.editingFinished.connect(self.updatePlotSettings)
        self.BV_settings_CB.currentTextChanged.connect(self.updatePlotSettings)
        self.updatePlotSettings()
        # Process tab initialization
        self.exp_directory_TB.clicked.connect(lambda: self.getExpDir(tab='process'))
        self.process_savesettings_PB.clicked.connect(self.saveProSettings)
        self.process_loadsettings_PB.clicked.connect(self.loadProSettings)
        self.run_start_PB.clicked.connect(self.startBatchProcessing)
        self.run_stop_PB.clicked.connect(self.stopProcess)
        # Modal tab initialization
        self.mdl_load_from_PB.clicked.connect(self.mdlLoadFrom)
        self.mdl_dir_TB.clicked.connect(lambda: self.getExpDir(tab='modal'))
        self.mdl_load_PB.clicked.connect(self.mdlLoadSettings)
        self.mdl_save_PB.clicked.connect(self.mdlSaveSettings)
        self.mdl_start_PB.clicked.connect(self.mdlStartProcessing)
        self.mdl_stop_PB.clicked.connect(self.stopProcess)

        # Create the maptlotlib FigureCanvas object
        self.valplot = MplCanvas(self, width=5, height=4, dpi=100)
        self.valplot.axes.text(5, 5, 'Add files to analize using the menubar... \n Then select a file from the list to plot', \
            ha='center', va='center',style='italic', size=12)
        self.valplot.axes.axis([0, 10, 0, 10])
        # Create toolbar, passing canvas as first parent
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

    def selectFiles(self):
        file_paths, ext = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files')
        self.updateList(file_paths=file_paths)

    def updateList(self, file_paths=None, setchange=None):
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
                self.file_list[key][1] = self.calculateMask(key=key)
        else:
            for key in self.file_list.keys():
                self.file_list[key][1] = self.calculateMask(key=key)
        for key in self.file_list.keys():
            item = QtWidgets.QTreeWidgetItem(self.files_TW) 
            item.setText(0, key)
            item.setText(1, str(int(np.sum(self.file_list[key][1]))))
            if key == current_key:
                self.files_TW.setCurrentItem(item)

    def clearList(self):
        self.files_TW.clear()
        self.file_list = {}
        self.valplot.axes.cla()
        self.valplot.draw()
        self.first_plot = True

    def showAbout(self):
        message = f"PIV Analysis Toolkit<br>Version {self.version}<br><br>PIV Analysis Toolkit is based on the \
            'OpenPIV' open-source project but with many enhanced capabilities.<br><a href='https://github.com\
            /pouya-m/openpiv-python/tree/PIV-Code-Pouya'>Github page</a><br><br>By Pouya Mohtat"
        msgBox = QtWidgets.QMessageBox.information(self, 'About', message)


    def calculateMask(self, key):
        u, v = self.file_list[key][2], self.file_list[key][3]
        
        if self.s2n_CB.isChecked():
            sig2noise = self.file_list[key][4]
            thr = float(self.s2n_LE.text())
            mask1 = validation.sig2noise_val( u, v, sig2noise, threshold = thr )
        else:
            mask1 = np.zeros(u.shape, dtype=bool)
            
        if self.global_velocity_CB.isChecked():
            ulim = [float(i) for i in self.global_uVelocity_LE.text().split(',')]
            vlim = [float(i) for i in self.global_vVelocity_LE.text().split(',')]
            mask2 = validation.global_val( u, v, (ulim[0], ulim[1]), (vlim[0], vlim[1]) )
        else:
            mask2 = np.zeros(u.shape, dtype=bool)

        if self.local_velocity_CB.isChecked():
            lim = [float(i) for i in self.local_velocity_LE.text().split(',')]
            ksize = int(self.local_kernel_LE.text())
            mask3 = validation.local_median_val(u, v, lim[0], lim[1], size=ksize)
        else:
            mask3 = np.zeros(u.shape, dtype=bool)

        if self.global_std_CB.isChecked():
            std = float(self.global_std_LE.text())
            mask4 = validation.global_std(u, v, std_threshold=std)
        else:
            mask4 = np.zeros(u.shape, dtype=bool)

        mask = mask1 | mask2 | mask3 | mask4
        return mask

    def updatePlot(self, current, previous=None):
        if self.files_TW.itemFromIndex(current):
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
    
    def updatePlotSettings(self):
        self.BV_settings = self.BV_settings_CB.currentText()
        self.valid_col, self.invalid_col, self.scale, self.width = self.plot_settings_LE.text().split(',')
        self.updatePlot(self.files_TW.currentIndex())

    def saveThrSettings(self):
        #getting the file path
        path, ext = QtWidgets.QFileDialog.getSaveFileName(self, \
            'Select a location to save the settings', 'Thresholding_Settings.dat')
        if path == '':
            return
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
        #saving to file
        with open(path, 'w') as fh:
            fh.write('Thresholding settings:\n')
            fh.write('{0:<30};{1:<15};{2:<15}\n'.format('Signal 2 Noise:', s2n_state, s2n_LE))
            fh.write('{0:<30};{1:<15};{2:<15};{3:<15}\n'.format('Global Velocity:', gv_state, gv_LE1, gv_LE2))
            fh.write('{0:<30};{1:<15};{2:<15};{3:<15}\n'.format('Local Median:', lv_state, lv_LE1, lv_LE2))
            fh.write('{0:<30};{1:<15};{2:<15}\n'.format('Global Std. Deviation:', gs_state, gs_LE))

    def loadThrSettings(self):
        #load and read file
        path, ext = QtWidgets.QFileDialog.getOpenFileName(self, \
            'Select settings file', 'Thresholding_Settings.dat')
        if path == '':
            return
        lines = []
        with open(path, 'r') as fh:
            for line in fh:
                lines.append(line[:-1])
        #extract and set values
        *_, s2n_state, s2n_LE = [lines[1].split(';')[i].strip() for i in range(3)]
        *_, gv_state, gv_LE1, gv_LE2 = [lines[2].split(';')[i].strip() for i in range(4)]
        *_, lv_state, lv_LE1, lv_LE2 = [lines[3].split(';')[i].strip() for i in range(4)]
        *_, gs_state, gs_LE = [lines[4].split(';')[i].strip() for i in range(3)]
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

        
    def getExpDir(self, tab):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Experiment Directory')
        if tab == 'process':
            self.exp_directory_LE.setText(dir_path)
        elif tab == 'modal':
            self.mdl_dir_LE.setText(dir_path)

    def saveProSettings(self, path=False):
        #getting the file path
        if path is False:
            path, ext = QtWidgets.QFileDialog.getSaveFileName(self, \
                'Select a location to save the settings', 'Process_Settings.dat')
        if path == '':
            return
        #getting the settings from GUI
        exp, pre, pro, pos = {}, {}, {}, {}
        exp['dir'] = self.exp_directory_LE.text()
        exp['exp'] = self.exp_experiments_LE.text()
        exp['run'] = self.exp_runs_LE.text()
        exp['patA'] = self.exp_patA_LE.text()
        exp['patB'] = self.exp_patB_LE.text()
        exp['nf'] = self.exp_nfiles_LE.text()
        pre['bg_st'] = str(self.pre_background_CB.isChecked())
        pre['bg_nf'] = self.pre_bg_nfiles_LE.text()
        pre['sm_st'] = str(self.pre_staticmask_CB.isChecked())
        pre['sm_pa'] = self.pre_sm_path_LE.text()
        pre['dm_st'] = str(self.pre_dynamicmask_CB.isChecked())
        pro['ws'] = self.pro_windowsize_LE.text()
        pro['sa'] = self.pro_searcharea_LE.text()
        pro['ol'] = self.pro_overlap_LE.text()
        pro['s2n'] = self.pro_sig2noise_CB.currentText()
        pro['ts'] = self.pro_timestep_LE.text()
        pro['sc'] = self.pro_scale_LE.text()
        pro['nc'] = self.pro_ncpus_LE.text()
        pos['s2n_st'] = str(self.pos_sig2noise_CB.isChecked())
        pos['s2n_ra'] = self.pos_s2n_ratio_LE.text()
        pos['gv_st'] = str(self.pos_globalvelocity_CB.isChecked())
        pos['gv_ul'] = self.pos_gv_ulim_LE.text()
        pos['gv_vl'] = self.pos_gv_vlim_LE.text()
        pos['std_st'] = str(self.pos_std_CB.isChecked())
        pos['std_ra'] = self.pos_std_LE.text()
        pos['lv_st'] = str(self.pos_localvelocity_CB.isChecked())
        pos['lv_df'] = self.pos_lv_uvdiff_LE.text()
        pos['lv_kr'] = self.pos_lv_kernel_LE.text()
        pos['bv_st'] = str(self.pos_badvector_CB.isChecked())
        pos['bv_mt'] = self.pos_bv_method_CB.currentText()
        pos['bv_ni'] = self.pos_bv_niterations_LE.text()
        pos['bv_kr'] = self.pos_bv_kernel_LE.text()
        pos['sm_st'] = str(self.pos_smoothing_CB.isChecked())
        pos['sm_ra'] = self.pos_smth_factor_LE.text()
        pos['fm_st'] = str(self.pos_fieldmanip_CB.isChecked())
        pos['fm_in'] = self.pos_fm_LE.text()
        pos['out_m'] = self.pos_output_CB.currentText()
        #saving to file
        postprocessing.saveSettings(exp, pre, pro, pos, path)

        return exp, pre, pro, pos      

    def loadProSettings(self):
        #load setting file
        path, ext = QtWidgets.QFileDialog.getOpenFileName(self, \
            'Select settings file', 'Process_Settings.dat')
        if path == '':
            return
        exp, pre, pro, pos = postprocessing.loadSettings(path)

        self.exp_directory_LE.setText(exp['dir'])
        self.exp_experiments_LE.setText(exp['exp'])
        self.exp_runs_LE.setText(exp['run'])
        self.exp_patA_LE.setText(exp['patA'])
        self.exp_patB_LE.setText(exp['patB'])
        self.exp_nfiles_LE.setText(exp['nf'])
        self.pre_background_CB.setChecked(eval(pre['bg_st']))
        self.pre_bg_nfiles_LE.setText(pre['bg_nf'])
        self.pre_staticmask_CB.setChecked(eval(pre['sm_st']))
        self.pre_sm_path_LE.setText(pre['sm_pa'])
        self.pre_dynamicmask_CB.setChecked(eval(pre['dm_st']))
        self.pro_windowsize_LE.setText(pro['ws'])
        self.pro_searcharea_LE.setText(pro['sa'])
        self.pro_overlap_LE.setText(pro['ol'])
        self.pro_sig2noise_CB.setCurrentText(pro['s2n'])
        self.pro_timestep_LE.setText(pro['ts'])
        self.pro_scale_LE.setText(pro['sc'])
        self.pro_ncpus_LE.setText(pro['nc'])
        self.pos_sig2noise_CB.setChecked(eval(pos['s2n_st']))
        self.pos_s2n_ratio_LE.setText(pos['s2n_ra'])
        self.pos_globalvelocity_CB.setChecked(eval(pos['gv_st']))
        self.pos_gv_ulim_LE.setText(pos['gv_ul'])
        self.pos_gv_vlim_LE.setText(pos['gv_vl'])
        self.pos_std_CB.setChecked(eval(pos['std_st']))
        self.pos_std_LE.setText(pos['std_ra'])
        self.pos_localvelocity_CB.setChecked(eval(pos['lv_st']))
        self.pos_lv_uvdiff_LE.setText(pos['lv_df'])
        self.pos_lv_kernel_LE.setText(pos['lv_kr'])
        self.pos_badvector_CB.setChecked(eval(pos['bv_st']))
        self.pos_bv_method_CB.setCurrentText(pos['bv_mt'])
        self.pos_bv_niterations_LE.setText(pos['bv_ni'])
        self.pos_bv_kernel_LE.setText(pos['bv_kr'])
        self.pos_smoothing_CB.setChecked(eval(pos['sm_st']))
        self.pos_smth_factor_LE.setText(pos['sm_ra'])
        self.pos_fieldmanip_CB.setChecked(eval(pos['fm_st']))
        self.pos_fm_LE.setText(pos['fm_in'])
        self.pos_output_CB.setCurrentText(pos['out_m'])

    
    def startBatchProcessing(self):
        if not os.path.isdir(self.exp_directory_LE.text()):
            QtWidgets.QMessageBox.warning(self, 'Experiment Directory Not Found!', 
                'The selected directory is not a valid path. Please select a valid directory in the "Run Settings" under "Experiment" tab...')
            return
        experiments = glob.glob(os.path.join(self.exp_directory_LE.text(), self.exp_experiments_LE.text()))
        for exp in experiments:
            setting_file = os.path.join(exp, 'Processing_Settings.dat')
            exp, pre, pro, pos = self.saveProSettings(setting_file)
        self.run_start_PB.setEnabled(False)
        manager = multiprocessing.Manager()
        self.processed_files = manager.list()
        self.piv_process_thread = PIVProcessThread(exp, pre, pro, pos, self.processed_files)
        self.piv_process_thread.progress_sig.connect(self.run_progress_TE.appendPlainText)
        self.piv_process_thread.finished.connect(lambda: self.finishProcess(tab='process'))
        self.piv_process_thread.start()
        #initialize the progress bars
        nrun = 0
        experiments =  glob.glob(os.path.join(exp['dir'], exp['exp']))
        for experiment in experiments:
            runs = glob.glob(os.path.join(experiment, exp['run']))
            nrun += len(runs)
        self.nf = int(exp['nf'])
        ntotal = self.nf*nrun
        self.run_progress_PBar.setEnabled(True)
        self.run_overalprogress_PBar.setEnabled(True)
        self.run_overalprogress_PBar.setRange(0, ntotal)
        self.run_progress_PBar.setRange(0, self.nf)
        self.run_overalprogress_PBar.setValue(0)
        self.run_progress_PBar.setValue(0)
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.updateProgressBar)
        self.progress_timer.start(200)

    def updateProgressBar(self):
        progress = len(self.processed_files)
        self.run_overalprogress_PBar.setValue(progress)
        if progress != 0:
            progress = progress % self.nf
            if progress == 0:
                progress = self.nf
        self.run_progress_PBar.setValue(progress)

    def finishProcess(self, tab):
        if tab == 'process':
            self.run_progress_TE.appendPlainText('All done!')
            self.progress_timer.stop()
            self.run_start_PB.setEnabled(True)
        elif tab == 'modal':
            self.mdl_progress_TE.appendPlainText('All done!')
            self.mdl_start_PB.setEnabled(True)

    def mdlLoadFrom(self):
        self.mdl_dir_LE.setText(self.exp_directory_LE.text())
        self.mdl_exp_LE.setText(self.exp_experiments_LE.text())
        self.mdl_run_LE.setText(self.exp_runs_LE.text())
        self.mdl_nf_LE.setText(self.exp_nfiles_LE.text())

    def mdlLoadSettings(self):
        #load setting file
        path, ext = QtWidgets.QFileDialog.getOpenFileName(self, \
            'Select settings file', 'Modal_Settings.dat')
        if path == '':
            return
        exp, analysis, rec = modal.ModalAnalysis.loadSettings(path)

        self.mdl_dir_LE.setText(exp['dir'])
        self.mdl_exp_LE.setText(exp['exp'])
        self.mdl_pat_LE.setText(exp['pat'])
        self.mdl_run_LE.setText(exp['run'])
        self.mdl_nf_LE.setText(exp['nf'])
        self.mdl_st_CB.setChecked(eval(analysis['st']))
        self.mdl_method_CB.setCurrentText(analysis['mt'])
        self.mdl_nm_LE.setText(analysis['nm'])
        self.mdl_rec_CB.setChecked(eval(rec['st']))
        self.mdl_rec_nm_LE.setText(rec['nm'])
        self.mdl_rec_ns_LE.setText(rec['ns'])

    def mdlSaveSettings(self, path=False):
        #getting the file path
        if path is False:
            path, ext = QtWidgets.QFileDialog.getSaveFileName(self, \
                'Select a location to save the settings', 'Modal_Settings.dat')
        if path == '':
            return
        #getting the settings from GUI
        exp, analysis, rec = {}, {}, {}
        exp['dir'] = self.mdl_dir_LE.text()
        exp['exp'] = self.mdl_exp_LE.text()
        exp['pat'] = self.mdl_pat_LE.text()
        exp['run'] = self.mdl_run_LE.text()
        exp['nf'] = self.mdl_nf_LE.text()
        analysis['st'] = str(self.mdl_st_CB.isChecked())
        analysis['mt'] = self.mdl_method_CB.currentText()
        analysis['nm'] = self.mdl_nm_LE.text()
        rec['st'] = str(self.mdl_rec_CB.isChecked())
        rec['nm'] = self.mdl_rec_nm_LE.text()
        rec['ns'] = self.mdl_rec_ns_LE.text()
        #saving to file
        modal.ModalAnalysis.saveSettings(exp, analysis, rec, path)

        return exp, analysis, rec

    def mdlStartProcessing(self):
        # save process settings
        if not os.path.isdir(self.mdl_dir_LE.text()):
            QtWidgets.QMessageBox.warning(self, 'Experiment Directory Not Found!', 
                'The selected directory is not a valid path. Please select a valid directory in the "Experiment" section...')
            return
        experiments = glob.glob(os.path.join(self.mdl_dir_LE.text(), self.mdl_exp_LE.text()))
        for experiment in experiments:
            setting_file = os.path.join(experiment, 'Modal_settings.dat')
            exp, analysis, rec = self.mdlSaveSettings(setting_file)
        # start the process thread 
        self.mdl_start_PB.setEnabled(False)
        self.mdl_progress_TE.clear()
        self.modal_process_thread = ModalProcessThread(exp, analysis, rec)
        self.modal_process_thread.progresstext_sig.connect(self.mdl_progress_TE.appendPlainText)
        self.modal_process_thread.progressbar_sig.connect(self.mdl_progress_PBar.setValue)
        self.modal_process_thread.finished.connect(lambda: self.finishProcess(tab='modal'))
        self.modal_process_thread.start()
        # set up the progress bar
        nrun = 0
        for experiment in experiments:
            runs = glob.glob(os.path.join(experiment, exp['run']))
            nrun += len(runs)
        self.mdl_progress_PBar.setEnabled(True)
        self.mdl_progress_PBar.setRange(0, nrun)
        self.mdl_progress_PBar.setValue(0)


    # still under development, better not use it (directly close the window instead!)
    def stopProcess(self):
        qm = QtWidgets.QMessageBox
        if self.Main_tabs.currentIndex() == 1:
            if hasattr(self, 'piv_process_thread'):
                ans = qm.question(self, "Stop Process", "Are you sure you want to stop the process?", \
                    buttons=qm.StandardButtons(qm.Yes | qm.No), defaultButton=qm.No)
                if ans == qm.No:
                    return
                # this does not work as it's supposed to, the processes are still running because they're busy in 'task.run'
                # loop and they don't check for exitting requests before they are done!
                self.piv_process_thread.quit()
                self.piv_process_thread.stop = True
                self.piv_process_thread.wait() 
                self.run_progress_PBar.setValue(0)
                self.run_overalprogress_PBar.setValue(0)
                self.run_start_PB.setEnabled(True)
                self.progress_timer.stop()
                self.run_progress_TE.appendPlainText('Progress stoped!')
        elif self.Main_tabs.currentIndex() == 3:
            if hasattr(self, 'modal_process_thread'):
                ans = qm.question(self, "Stop Process", "Are you sure you want to stop the process?", \
                    buttons=qm.StandardButtons(qm.Yes | qm.No), defaultButton=qm.No)
                if ans == qm.No:
                    return
                self.modal_process_thread.quit()
                self.mdl_progress_PBar.setValue(0)
                self.mdl_start_PB.setEnabled(True)
                self.mdl_progress_TE.appendPlainText('Progress Stoped!')


class ModalProcessThread(QThread):

    def __init__(self, exp, analysis, rec):
        super(ModalProcessThread, self).__init__()
        self.exp, self.analysis, self.rec = exp, analysis, rec
        self.progress = 0

    progresstext_sig = Signal(str)
    progressbar_sig = Signal(int)

    def run(self):
        experiments = glob.glob(os.path.join(self.exp['dir'], self.exp['exp']))
        experiments.sort()
        for experiment in experiments:
            runs = glob.glob(os.path.join(experiment, self.exp['run']))
            runs.sort()
            for run in runs:
                path = os.path.join(run, 'Analysis')
                self.progresstext_sig.emit(f'modal analysis: {run}')
                modal_analysis = modal.ModalAnalysis(path, nfiles=int(self.exp['nf']), pattern=self.exp['pat'])
                if self.analysis['st'] == 'True':
                    if self.analysis['mt'] == 'Singular Value Decomposition':
                        self.progresstext_sig.emit('runing SVD...')
                        modal_analysis.svd(nmode=int(self.analysis['nm']))
                    elif self.analysis['mt'] == 'Snapshots Method':
                        self.progresstext_sig.emit('runing snapshots method...')
                        modal_analysis.snapshot(nmode=int(self.analysis['nm']))
                if self.rec['st'] == 'True':
                    self.progresstext_sig.emit('recontructing flow field...')
                    modal_analysis.reconstructField(nmode=int(self.rec['nm']), nsp=int(self.rec['ns']))
                self.progress += 1
                self.progressbar_sig.emit(self.progress)

class PIVProcessThread(QThread):

    def __init__(self, exp, pre, pro, pos, processed_files):
        super(PIVProcessThread, self).__init__()
        self.exp, self.pre, self.pro, self.pos = exp, pre, pro, pos
        self.processed_files = processed_files
        self.stop = False
        self.stop_timer = QTimer(self)
        self.stop_timer.timeout.connect(self.stopProcess)
        self.stop_timer.start(500)
        
    progress_sig = Signal(str)  #signals have to be defined as class variables

    def run(self):
        experiments = glob.glob(os.path.join(self.exp['dir'], self.exp['exp']))
        experiments.sort()
        for experiment in experiments:
            runs = glob.glob(os.path.join(experiment, self.exp['run']))
            runs.sort()
            for run in runs:
                
                # prepare data directories
                analysis_path = tools.create_directory(run)                #creates the Analysis folder if not already there
                tools.create_directory(analysis_path, folder='Unvalidated')     #creates the Unvalidated folder if not already there
                data_dir = os.path.join(run, 'RawData')
                
                # preprocess
                self.progress_sig.emit(f'Processing run: {run} ')
                task = tools.Multiprocesser( data_dir=data_dir, pattern_a=self.exp['patA'], pattern_b=self.exp['patB'] )
                if self.pre['bg_st'] == 'True':
                    bga_file = os.path.join(analysis_path, 'background_a.TIF')
                    bgb_file = os.path.join(analysis_path, 'background_b.TIF')
                    if ( os.path.exists(bga_file) and os.path.exists(bgb_file) ):
                        self.progress_sig.emit('using existing background files...')
                        background_a = tools.imread(bga_file)
                        background_b = tools.imread(bgb_file)
                    else:
                        self.progress_sig.emit('finding background...')
                        background_a, background_b = task.find_background2(n_files=int(self.pre['bg_nf']))
                        imsave(os.path.join(analysis_path, 'background_a.TIF'), background_a)
                        imsave(os.path.join(analysis_path, 'background_b.TIF'), background_b)
                else:
                    background_a, background_b = None, None
                
                # piv+post process
                self.progress_sig.emit('main process...')
                task.n_files = int(self.exp['nf'])
                Process = partial(mainPIVProcess, bga=background_a, bgb=background_b, pro=self.pro, pos=self.pos, processed_files=self.processed_files)
                data = task.run( func = Process, n_cpus=int(self.pro['nc']) )
                
                # extended output
                if self.pos['out_m'] == 'extended':
                    self.progress_sig.emit('calculating extended output...')
                    # initialize variables to hold data
                    im_file, *_ = glob.glob(os.path.join(data_dir, self.exp['patA']))
                    image = tools.imread(im_file)
                    x, y = pyprocess.get_coordinates(image.shape, int(self.pro['ws']), int(self.pro['ol']))
                    # do field manipulation and scaling on x and y
                    if self.pos['fm_st'] == 'True':
                        for fm in self.pos['fm_in'].split(','):
                            x, y, *_ = tools.manipulate_field(x, y, x, x, x, mode=fm.strip())
                    scale = float(self.pro['sc'])
                    x, y = x/scale, y/scale
                    u, v, mask, vor, velMag = np.zeros((5, x.shape[0], x.shape[1], int(self.exp['nf'])), np.float)
                    basename = np.zeros((int(self.exp['nf']),), 'U50')
                    # extract data
                    for n, D in enumerate(data):
                        basename[n], u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n] = D
                    del(data)
                    # calculate mean values
                    um, vm, vorm = u.mean(axis=2), v.mean(axis=2), vor.mean(axis=2)
                    # calculate fluctuations
                    up = u - um[...,np.newaxis]
                    vp = v - vm[...,np.newaxis]
                    upvp = up * vp
                    TKE = 0.5 * (up*up + vp*vp)
                    upupm = (up*up).mean(axis=2)
                    vpvpm = (vp*vp).mean(axis=2)
                    upvpm = upvp.mean(axis=2)
                    TKE_rms = 0.5 * (upupm + vpvpm)
                    # save the results
                    avg_file = os.path.join(analysis_path, 'AVG.dat')
                    header = '"x", "y", "u_avg", "v_avg", "vorticity_avg", "upup_avg", "vpvp_avg", "upvp_avg", "TKE_rms"'
                    tools.save( x, y, filename=avg_file, variables=[um, vm, vorm, upupm, vpvpm, upvpm, TKE_rms], header=header )

                    header = '"x", "y", "u", "v", "mask", "vorticity", "velocity magnitude", "up", "vp", "upvp", "TKE"'
                    for n, bn in enumerate(basename):
                        fname = os.path.join(analysis_path, bn)
                        tools.save( x, y, filename=fname, variables=[u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n], up[:,:,n], vp[:,:,n], upvp[:,:,n], TKE[:,:,n]], header=header )
                
        return True

    #does not work as intended (timer event is ignored because the program is busy running the 'task.run' function)
    def stopProcess(self):
        if self.stop == True:
            self.quit()
            print('trying to quit...')


def mainPIVProcess( args, bga, bgb, pro, pos, processed_files):
    # unpacking the arguments
    file_a, file_b, counter = args
    # read images
    frame_a  = tools.imread( file_a )
    frame_b  = tools.imread( file_b )
    # background removal
    if bga is not None:
        frame_a = frame_a - bga
        frame_b = frame_b - bgb
    # process image pair with piv algorithm.
    u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, \
        window_size=int(pro['ws']), overlap=int(pro['ol']), dt=float(pro['ts']), search_area_size=int(pro['sa']), sig2noise_method=pro['s2n'])
    x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=int(pro['ws']), overlap=int(pro['ol']) )
    save_path = tools.create_path(file_a, folders=['Analysis', 'Unvalidated'])
    tools.save(x, y, u, v, sig2noise, save_path)
    #post processing
    #validation
    mask = np.zeros(u.shape, dtype=bool)
    if pos['s2n_st'] == 'True':
        mask1 = validation.sig2noise_val( u, v, sig2noise, threshold = float(pos['s2n_ra']) )
        mask = mask | mask1
    if pos['gv_st'] == 'True':
        umin, umax = map(float, pos['gv_ul'].split(','))
        vmin, vmax = map(float, pos['gv_vl'].split(','))
        mask2 = validation.global_val( u, v, (umin, umax), (vmin, vmax) )
        mask = mask | mask2
    if pos['lv_st'] == 'True':
        udif, vdif = map(float, pos['lv_df'].split(','))
        mask3 = validation.local_median_val(u, v, udif, vdif, size=int(pos['lv_kr']))
        mask = mask | mask3
    if pos['std_st'] == 'True':
        mask4 = validation.global_std(u, v, std_threshold=float(pos['std_ra']))
        mask = mask | mask4
    # vector corrections
    if pos['bv_st'] == 'True':
        u[mask], v[mask] = np.nan, np.nan
        u, v = filters.replace_outliers( u, v, method=pos['bv_mt'], max_iter=int(pos['bv_ni']), kernel_size=int(pos['bv_kr']))
    if pos['sm_st'] == 'True':
        u_ra, v_ra = map(float, pos['sm_ra'].split(','))
        u, *_ = smoothn.smoothn(u, s=u_ra)
        v, *_ = smoothn.smoothn(v, s=v_ra)
    if pos['fm_st'] == 'True':
        for fm in pos['fm_in'].split(','):
            x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode=fm.strip())
    # scaling
    scale = float(pro['sc'])
    x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = scale)
    # calculate vorticity and velocity magnitude
    vor = postprocessing.vorticity(u, v, x, y)
    velMag = np.sqrt(u*u + v*v)
    # update processed files, then save or return values
    processed_files.append(save_path)
    if pos['out_m'] == 'simple':
        header = '"x", "y", "u", "v", "mask", "vorticity", "velocity magnitude"'
        fname = tools.create_path(file_a)
        tools.save(x, y, filename=fname, variables=[u, v, mask, vor, velMag], header=header)
    else:
        basename = os.path.basename(save_path)
        return basename, u, v, mask, vor, velMag
       


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle('Fusion')
    dirname = os.path.dirname(__file__)
    app.setWindowIcon(QIcon(os.path.join(dirname, 'PIV.ico')))
    app.setStyleSheet(open(os.path.join(dirname, 'StyleSheet.qss'), 'r').read())
    #styles.dark(app)
    main_piv = MainPIV()
    sys.exit(app.exec_())
