
from PySide2 import QtWidgets
from PySide2.QtCore import QThread, Signal
import Main_PIV
import ImportDialog_Val as ImportDialog_Val
from openpiv import tools, validation, filters, pyprocess, scaling
from openpiv.smoothn import smoothn
import numpy as np
import os, time
from functools import partial
import multiprocessing
from imageio import imsave


import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class ImportDialog(ImportDialog_Val.Ui_ImportDialog_Val, QtWidgets.QDialog):

    def __init__(self):
        super(ImportDialog, self).__init__()
        self.setupUi(self)
        self.folderPath_TB.clicked.connect(self.selectFiles)
        self.addFiles_PB.clicked.connect(self.addFiles)
        self.cancel_PB.clicked.connect(self.close)

    def selectFiles(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder Containing Raw Images')
        self.folderPath_LE.setText(dir_path)

    def addFiles(self):
        settings = {}
        settings['DP']= self.folderPath_LE.text()
        settings['P_a'] = self.patternA_LE.text()
        settings['P_b'] = self.patternB_LE.text()
        settings['N_f'] = int(self.nFiles_LE.text())
        settings['WS'] = int(self.windowSize_LE.text())
        settings['OL'] = int(self.overlap_LE.text())
        settings['DT'] = float(self.timeStep_LE.text())
        settings['SA'] = int(self.searchSize_LE.text())
        settings['S2N'] = self.sig2noise_CB.currentText()
        settings['N_cpu'] = int(self.ncpus_LE.text())
        manager = multiprocessing.Manager()
        self.processed_files = manager.list()
        self.import_process_thread = ImportProcessThread(settings, self.processed_files)
        self.import_process_thread.start()
        self.import_process_thread.finished.connect(self.finishSimpleProcess)
        
        self.progressBar.setRange(0, settings['N_f'])
        self.progressBar.setValue(0)
        self.import_pbar_thread = ImportPBarThread(self.processed_files, settings['N_f'])
        self.import_pbar_thread.progress_sig.connect(self.progressBar.setValue)
        self.import_pbar_thread.start()

    def finishSimpleProcess(self):
        MainPIV.updateList(main_piv, file_paths=self.processed_files)
        #self.import_process_thread.quit()
        #self.import_pbar_thread.quit()
        self.close()


class ImportPBarThread(QThread):

    def __init__(self, processed_files, n_files):
        super(ImportPBarThread, self).__init__()
        self.processed_files = processed_files
        self.n_files = n_files
    
    progress_sig = Signal(int) #has to be defined as class variable

    def run(self):
        last_value = 0
        while last_value < self.n_files:
            time.sleep(0.2)
            try:
                new_value = len(self.processed_files)
            except BrokenPipeError:
                new_value = self.n_files
            if last_value != new_value:
                self.progress_sig.emit(new_value)
                last_value = new_value
    

class ImportProcessThread(QThread):

    def __init__(self, settings, processed_files):
        super(ImportProcessThread, self).__init__()
        self.stg = settings
        self.processed_files = processed_files

    def run(self):
        Run_path = os.path.dirname(self.stg['DP'])
        tools.create_directory(Run_path, folder='Analysis')
        tools.create_directory(Run_path, folder='Analysis/Validation')
        task = tools.Multiprocesser( data_dir=self.stg['DP'], pattern_a=self.stg['P_a'], pattern_b=self.stg['P_b'] )
        task.n_files = self.stg['N_f']
        process = partial(simpleProcess, processed_files=self.processed_files, WS=self.stg['WS'], OL=self.stg['OL'], \
            DT=self.stg['DT'], SA=self.stg['SA'], S2N=self.stg['S2N'])
        task.run( func = process, n_cpus=self.stg['N_cpu'] )


class MainPIV(Main_PIV.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(MainPIV, self).__init__()
        self.setupUi(self)
        #self.showMaximized()
        self.setWindowTitle('PIV - Build 003')
        self.resize(1280, 800)
        self.file_list = {}
        self.first_plot = True
        self.actionLoad_Files.triggered.connect(self.selectFiles)
        self.actionExit.triggered.connect(qApp.quit)
        self.actionLoad_Raw_Images.triggered.connect(self.openRawImages)
        self.actionClear_Files.triggered.connect(self.clearList)
        self.apply_settings_PB.clicked.connect(lambda: self.updateList(setchange=1))
        self.load_settings_PB.clicked.connect(self.loadThrSettings)
        self.save_settings_PB.clicked.connect(self.saveThrSettings)
        selmodel = self.files_TW.selectionModel()
        selmodel.currentChanged.connect(self.updatePlot)
        self.plot_settings_LE.editingFinished.connect(self.updatePlotSettings)
        self.BV_settings_CB.currentTextChanged.connect(self.updatePlotSettings)
        self.updatePlotSettings()
        # Process tab initialization
        self.process_savesettings_PB.clicked.connect(self.saveProSettings)
        self.process_loadsettings_PB.clicked.connect(self.loadProSettings)
        self.run_start_PB.clicked.connect(self.StartBatchProcessing)

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
        self.show()

    def selectFiles(self):
        file_paths, ext = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Files')
        self.updateList(file_paths=file_paths)

    def updateList(self, file_paths=None, setchange=None):
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
        dt = time.time()-t1
        print(f'BV calculated in {dt:.2f} sec')

    def clearList(self):
        self.files_TW.clear()
        self.file_list = {}
        self.valplot.axes.cla()
        self.valplot.draw()
        self.first_plot = True

    def calculateMask(self, key):
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

    def updatePlot(self, current, previous=None):
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

    def openRawImages(self):
        import_dialog = ImportDialog()
        import_dialog.exec_()

    def saveProSettings(self, path=False):
        #getting the file path
        if path is False:
            path, ext = QtWidgets.QFileDialog.getSaveFileName(self, \
                'Select a location to save the settings', 'Process_Settings.dat')
        if path == '':
            return
        #getting the settings
        exp, pre, pro, pos = {}, {}, {}, {}
        exp['dir'] = self.exp_directory_LE.text()
        exp['exp'] = self.exp_experiments_LE.text()
        exp['run'] = self.exp_runs_LE.text()
        exp['patA'] = self.exp_patA_LE.text()
        exp['patB'] = self.exp_patB_LE.text()
        exp['nf'] = self.exp_nfiles_LE.text()
        pre['bg_st'] = str(self.pre_background_CB.isChecked())
        pre['bg_nf'] = self.pre_bg_nfiles_LE.text()
        pre['bg_cs'] = self.pre_bg_chunksize_LE.text()
        pre['bg_nc'] = self.pre_bg_ncpus_LE.text()
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
        #saving to file
        with open(path, 'w') as fh:
            fh.write('Process settings:\n\n')
            fh.write('Experiment:\n\t{0:<30};'.format('Directory:'))
            fh.write('{0}\n\t{1:<30};{2}\n\t{3:<30};{4}\n'.format(exp['dir'], 'Experiments:', exp['exp'], 'Runs:', exp['run']))
            fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15}\n\n'.format('Files:', exp['patA'], exp['patB'], exp['nf']))
            fh.write('Pre-Process:\n\t{0:<30};{1:<15};{2:<15};{3:<15};{4:<15}\n'.format('Remove Background:', pre['bg_st'], pre['bg_nf'], pre['bg_cs'], pre['bg_nc']))
            fh.write('\t{0:<30};{1:<15};{2:<15}\n'.format('Static Mask:', pre['sm_st'], pre['sm_pa']))
            fh.write('\t{0:<30};{1:<15}\n\n'.format('Dynamic Mask:', pre['dm_st']))
            fh.write('Process:\n\t{0:<30};{1:<15}\n\t{2:<30};{3:<15}\n\t{4:<30};{5:<15}\n'.format('Window Size:', pro['ws'], 'Search Area Size:', pro['sa'], 'Overlap:', pro['ol']))
            fh.write('\t{0:<30};{1:<15}\n\t{2:<30};{3:<15}\n\t{4:<30};{5:<15}\n'.format('Signal/Noise Method:', pro['s2n'], 'Time Step:', pro['ts'], 'Scale:', pro['sc']))
            fh.write('\t{0:<30};{1:<15}\n\n'.format('Number of CPUs:', pro['nc']))
            fh.write('Post-process:\n\t{0:<30};{1:<15};{2:<15}\n'.format('Signal/Noise:', pos['s2n_st'], pos['s2n_ra']))
            fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15}\n'.format('Global Velocity:', pos['gv_st'], pos['gv_ul'], pos['gv_vl']))
            fh.write('\t{0:<30};{1:<15};{2:<15}\n'.format('Global Standard Deviation:', pos['std_st'], pos['std_ra']))
            fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15}\n'.format('Local Velocity:', pos['lv_st'], pos['lv_df'], pos['lv_kr']))
            fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15};{4:<15}\n'.format('Bad Vector Replacement:', pos['bv_st'], pos['bv_mt'], pos['bv_ni'], pos['bv_kr']))
            fh.write('\t{0:<30};{1:<15};{2:<15}\n\t{3:<30};{4:<15};{5:<15}\n'.format('Vector Smoothing:', pos['sm_st'], pos['sm_ra'], 'Field Manipulation:', pos['fm_st'], pos['fm_in']))

        return exp, pre, pro, pos      

    def loadProSettings(self):
        #load and read file
        path, ext = QtWidgets.QFileDialog.getOpenFileName(self, \
            'Select settings file', 'Process_Settings.dat')
        if path == '':
            return
        lines = []
        with open(path, 'r') as fh:
            for line in fh:
                lines.append(line[:-1])
        #extract and set values
        exp, pre, pro, pos = {}, {}, {}, {}
        *_, exp['dir'] = lines[3].split(';')
        *_, exp['exp'] = lines[4].split(';')
        *_, exp['run'] = lines[5].split(';')
        *_, exp['patA'], exp['patB'], exp['nf'] = [lines[6].split(';')[i].strip() for i in range(4)]
        *_, pre['bg_st'], pre['bg_nf'], pre['bg_cs'], pre['bg_nc'] = [lines[9].split(';')[i].strip() for i in range(5)]
        *_, pre['sm_st'], pre['sm_pa'] = [lines[10].split(';')[i].strip() for i in range(3)]
        *_, pre['dm_st'] = [lines[11].split(';')[i].strip() for i in range(2)]
        *_, pro['ws'] = [lines[14].split(';')[i].strip() for i in range(2)]
        *_, pro['sa'] = [lines[15].split(';')[i].strip() for i in range(2)]
        *_, pro['ol'] = [lines[16].split(';')[i].strip() for i in range(2)]
        *_, pro['s2n'] = [lines[17].split(';')[i].strip() for i in range(2)]
        *_, pro['ts'] = [lines[18].split(';')[i].strip() for i in range(2)]
        *_, pro['sc'] = [lines[19].split(';')[i].strip() for i in range(2)]
        *_, pro['nc'] = [lines[20].split(';')[i].strip() for i in range(2)]
        *_, pos['s2n_st'], pos['s2n_ra'] = [lines[23].split(';')[i].strip() for i in range(3)]
        *_, pos['gv_st'], pos['gv_ul'], pos['gv_vl'] = [lines[24].split(';')[i].strip() for i in range(4)]
        *_, pos['std_st'], pos['std_ra'] = [lines[25].split(';')[i].strip() for i in range(3)]
        *_, pos['lv_st'], pos['lv_df'], pos['lv_kr'] = [lines[26].split(';')[i].strip() for i in range(4)]
        *_, pos['bv_st'], pos['bv_mt'], pos['bv_ni'], pos['bv_kr'] = [lines[27].split(';')[i].strip() for i in range(5)]
        *_, pos['sm_st'], pos['sm_ra'] = [lines[28].split(';')[i].strip() for i in range(3)]
        *_, pos['fm_st'], pos['fm_in'] = [lines[29].split(';')[i].strip() for i in range(3)]

        self.exp_directory_LE.setText(exp['dir'])
        self.exp_experiments_LE.setText(exp['exp'])
        self.exp_runs_LE.setText(exp['run'])
        self.exp_patA_LE.setText(exp['patA'])
        self.exp_patB_LE.setText(exp['patB'])
        self.exp_nfiles_LE.setText(exp['nf'])
        self.pre_background_CB.setChecked(eval(pre['bg_st']))
        self.pre_bg_nfiles_LE.setText(pre['bg_nf'])
        self.pre_bg_chunksize_LE.setText(pre['bg_cs'])
        self.pre_bg_ncpus_LE.setText(pre['bg_nc'])
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

    
    def StartBatchProcessing(self):
        if os.path.isdir(self.exp_directory_LE.text()):
            directory = os.path.join(self.exp_directory_LE.text(), 'Processing_Settings.dat')
        else:
            QtWidgets.QMessageBox.warning(self, 'Experiment Directory Not Found!', 'The selected directory is not a valid path. Please select a valid directory in the "Run Settings" under "Experiment" tab...')
            return
        exp, pre, pro, pos = self.saveProSettings(directory)
        self.run_start_PB.setEnabled(False)
        manager = multiprocessing.Manager()
        self.processed_files = manager.list()
        self.batch_process_thread = BatchProcessThread(exp, pre, pro, pos, self.processed_files, self.run_progress_TE)
        self.batch_process_thread.start()
        self.batch_process_thread.finished.connect(self.finishBatchProcess)

        nrun = len(exp['run'].split(','))
        nexp = len(exp['exp'].split(','))
        self.nf = int(exp['nf'])
        ntotal = self.nf*nrun*nexp
        self.run_overalprogress_PBar.setRange(0, ntotal)
        self.run_progress_PBar.setRange(0, self.nf)
        self.run_overalprogress_PBar.setValue(0)
        self.run_progress_PBar.setValue(0)
        self.batch_pbar_thread = BatchPBarThread(self.processed_files, ntotal)
        self.batch_pbar_thread.progress_sig.connect(self.setProgress)
        self.batch_pbar_thread.start()


    def setProgress(self, progress):
        self.run_overalprogress_PBar.setValue(progress)
        progress = progress % self.nf
        if (progress == 0):
            progress = self.nf
        self.run_progress_PBar.setValue(progress)

    
    def finishBatchProcess(self):
        #self.run_progress_TE.clear()
        self.run_progress_TE.appendPlainText('all done!')
        self.run_progress_TE.ensureCursorVisible()
        self.run_start_PB.setEnabled(True)


class BatchProcessThread(QThread):

    def __init__(self, exp, pre, pro, pos, processed_files, TE):
        super(BatchProcessThread, self).__init__()
        self.exp, self.pre, self.pro, self.pos = exp, pre, pro, pos
        self.processed_files = processed_files
        self.TE = TE

    def run(self):
        for experiment in self.exp['exp'].split(','):
            for run in self.exp['run'].split(','):
                experiment, run = experiment.strip(), run.strip()
                run_path = os.path.join(os.path.join(self.exp['dir'], experiment), run)
                analysis_path = tools.create_directory(run_path) #creates the Analysis folder if not already there
                #self.TE.clear()
                self.TE.appendPlainText(f'Processing run: {experiment} / {run}')
                self.TE.ensureCursorVisible()
                data_dir = os.path.join(run_path, 'Raw Data')
                task = tools.Multiprocesser( data_dir=data_dir, pattern_a=self.exp['patA'], pattern_b=self.exp['patB'] )
                # preprocess
                if self.pre['bg_st'] == 'True':
                    self.TE.appendPlainText('finding bg...')
                    self.TE.ensureCursorVisible()
                    background_a, background_b = task.find_background(n_files=int(self.pre['bg_nf']), chunk_size=int(self.pre['bg_cs']), n_cpus=int(self.pre['bg_nc']))
                    imsave(os.path.join(analysis_path, 'background_a.TIF'), background_a)
                    imsave(os.path.join(analysis_path, 'background_b.TIF'), background_b)
                else:
                    background_a, background_b = None, None
                # main process
                self.TE.appendPlainText('main process...')
                self.TE.ensureCursorVisible()
                task.n_files = int(self.exp['nf'])
                Process = partial(batchProcess, bga=background_a, bgb=background_b, pro=self.pro, pos=self.pos, processed_files=self.processed_files)
                task.run( func = Process, n_cpus=int(self.pro['nc']) )
                #print(self.processed_files)


class BatchPBarThread(QThread):

    def __init__(self, processed_files, nf):
        super(BatchPBarThread, self).__init__()
        self.processed_files = processed_files
        self.nf = nf
    
    progress_sig = Signal(int) #has to be defined as class variable

    def run(self):
        last_value = 0
        while last_value < self.nf:
            time.sleep(0.2)
            try:
                new_value = len(self.processed_files)
            except BrokenPipeError:
                new_value = self.nf
            if last_value != new_value:
                self.progress_sig.emit(new_value)
                last_value = new_value


def batchProcess( args, bga, bgb, pro, pos, processed_files):
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
    save_path = tools.create_path(file_a, folder='Analysis')
    tools.save(x, y, u, v, sig2noise, save_path+'_unvalidated.dat')
    # validation
    mask = np.zeros(u.shape, dtype=bool)
    if pos['s2n_st'] == 'True':
        u, v, mask1 = validation.sig2noise_val( u, v, sig2noise, threshold = float(pos['s2n_ra']) )
        mask = mask | mask1
    if pos['gv_st'] == 'True':
        umin, umax = pos['gv_ul'].split(',')
        vmin, vmax = pos['gv_vl'].split(',')
        u, v, mask2 = validation.global_val( u, v, (float(umin), float(umax)), (float(vmin), float(vmax)) )
        mask = mask | mask2
    if pos['lv_st'] == 'True':
        udif, vdif = pos['lv_df'].split(',')
        u, v, mask3 = validation.local_median_val(u, v, float(udif), float(vdif), size=int(pos['lv_kr']))
        mask = mask | mask3
    if pos['std_st'] == 'True':
        u, v, mask4 = validation.global_std(u, v, std_threshold=float(pos['std_ra']))
        mask = mask | mask4
    # vector corrections
    if pos['bv_st'] == 'True':
        u, v = filters.replace_outliers( u, v, method=pos['bv_mt'], max_iter=int(pos['bv_ni']), kernel_size=int(pos['bv_kr']))
    if pos['sm_st'] == 'True':
        u_ra, v_ra = pos['sm_ra'].split(',')
        u, *_ = smoothn(u, s=float(u_ra))
        v, *_ = smoothn(v, s=float(v_ra))
    if pos['fm_st'] == 'True':
        for fm in pos['fm_in'].split(','):
            x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode=fm.strip())
    # scaling and saving the final results
    x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = float(pro['sc']))
    tools.save(x, y, u, v, mask, save_path+'.dat')
    processed_files.append(save_path+'.dat')
       


def simpleProcess( args, processed_files, WS, OL, DT, SA, S2N):
    # unpacking the arguments
    file_a, file_b, counter = args
    # read images into numpy arrays
    frame_a  = tools.imread( file_a )
    frame_b  = tools.imread( file_b )
    # process image pair with piv algorithm.
    u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, \
        window_size=WS, overlap=OL, dt=DT, search_area_size=SA, sig2noise_method=S2N)
    x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=WS, overlap=OL )
    save_path = tools.create_path(file_a, folder='Analysis')
    tools.save(x, y, u, v, sig2noise, save_path+'_unvalidated.dat')
    processed_files.append(save_path+'.dat')


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    #app.setStyle('Fusion')
    main_piv = MainPIV()
    app.exec_()

