
#(MIN-env) C:\Users\Asus\Desktop\UI>python C:\Users\Asus\anaconda3\envs\MIN-env\Library\bin\pyside2-uic ImportDialog_Val.ui 
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImportDialog_Val.ui',
# licensing of 'ImportDialog_Val.ui' applies.
#
# Created: Wed Jul 15 09:50:07 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ImportDialog_Val(object):
    def setupUi(self, ImportDialog_Val):
        ImportDialog_Val.setObjectName("ImportDialog_Val")
        ImportDialog_Val.resize(680, 425)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ImportDialog_Val)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileSelection_GB = QtWidgets.QGroupBox(ImportDialog_Val)
        self.fileSelection_GB.setObjectName("fileSelection_GB")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.fileSelection_GB)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.fileSelection_GB)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.folderPath_TB = QtWidgets.QToolButton(self.fileSelection_GB)
        self.folderPath_TB.setObjectName("folderPath_TB")
        self.gridLayout.addWidget(self.folderPath_TB, 0, 4, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.fileSelection_GB)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.fileSelection_GB)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)
        self.patternA_LE = QtWidgets.QLineEdit(self.fileSelection_GB)
        self.patternA_LE.setPlaceholderText("")
        self.patternA_LE.setObjectName("patternA_LE")
        self.gridLayout.addWidget(self.patternA_LE, 1, 1, 1, 1)
        self.nFiles_LE = QtWidgets.QLineEdit(self.fileSelection_GB)
        self.nFiles_LE.setPlaceholderText("")
        self.nFiles_LE.setObjectName("nFiles_LE")
        self.gridLayout.addWidget(self.nFiles_LE, 2, 1, 1, 1)
        self.folderPath_LE = QtWidgets.QLineEdit(self.fileSelection_GB)
        self.folderPath_LE.setObjectName("folderPath_LE")
        self.gridLayout.addWidget(self.folderPath_LE, 0, 0, 1, 4)
        self.patternB_LE = QtWidgets.QLineEdit(self.fileSelection_GB)
        self.patternB_LE.setPlaceholderText("")
        self.patternB_LE.setObjectName("patternB_LE")
        self.gridLayout.addWidget(self.patternB_LE, 1, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.fileSelection_GB)
        self.preprocessSettings_GB = QtWidgets.QGroupBox(ImportDialog_Val)
        self.preprocessSettings_GB.setObjectName("preprocessSettings_GB")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.preprocessSettings_GB)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.windowSize_LE = QtWidgets.QLineEdit(self.preprocessSettings_GB)
        self.windowSize_LE.setObjectName("windowSize_LE")
        self.gridLayout_3.addWidget(self.windowSize_LE, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.preprocessSettings_GB)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 3, 1, 1)
        self.searchSize_LE = QtWidgets.QLineEdit(self.preprocessSettings_GB)
        self.searchSize_LE.setObjectName("searchSize_LE")
        self.gridLayout_3.addWidget(self.searchSize_LE, 0, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.preprocessSettings_GB)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 5, 1, 1)
        self.overlap_LE = QtWidgets.QLineEdit(self.preprocessSettings_GB)
        self.overlap_LE.setObjectName("overlap_LE")
        self.gridLayout_3.addWidget(self.overlap_LE, 0, 6, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.preprocessSettings_GB)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 2)
        self.ncpus_LE = QtWidgets.QLineEdit(self.preprocessSettings_GB)
        self.ncpus_LE.setObjectName("ncpus_LE")
        self.gridLayout_3.addWidget(self.ncpus_LE, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.preprocessSettings_GB)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.timeStep_LE = QtWidgets.QLineEdit(self.preprocessSettings_GB)
        self.timeStep_LE.setObjectName("timeStep_LE")
        self.gridLayout_3.addWidget(self.timeStep_LE, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.preprocessSettings_GB)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.preprocessSettings_GB)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 3, 1, 1)
        self.sig2noise_CB = QtWidgets.QComboBox(self.preprocessSettings_GB)
        self.sig2noise_CB.setObjectName("sig2noise_CB")
        self.sig2noise_CB.addItem("")
        self.sig2noise_CB.addItem("")
        self.sig2noise_CB.addItem("")
        self.gridLayout_3.addWidget(self.sig2noise_CB, 1, 4, 1, 2)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.preprocessSettings_GB)
        self.progressBar = QtWidgets.QProgressBar(ImportDialog_Val)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addFiles_PB = QtWidgets.QPushButton(ImportDialog_Val)
        self.addFiles_PB.setObjectName("addFiles_PB")
        self.horizontalLayout.addWidget(self.addFiles_PB)
        self.cancel_PB = QtWidgets.QPushButton(ImportDialog_Val)
        self.cancel_PB.setObjectName("cancel_PB")
        self.horizontalLayout.addWidget(self.cancel_PB)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ImportDialog_Val)
        QtCore.QMetaObject.connectSlotsByName(ImportDialog_Val)

    def retranslateUi(self, ImportDialog_Val):
        ImportDialog_Val.setWindowTitle(QtWidgets.QApplication.translate("ImportDialog_Val", "Add Raw Image Files For Validation", None, -1))
        self.fileSelection_GB.setTitle(QtWidgets.QApplication.translate("ImportDialog_Val", "File Selection", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Pattern A", None, -1))
        self.folderPath_TB.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "...", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Pattern B", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Num.of Files", None, -1))
        self.patternA_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "*LA.TIF", None, -1))
        self.nFiles_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "4", None, -1))
        self.folderPath_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "C:\\Users\\Asus\\Desktop\\UI\\Dummy Data\\Raw Data", None, -1))
        self.folderPath_LE.setPlaceholderText(QtWidgets.QApplication.translate("ImportDialog_Val", "Enter Folder Path Containing Raw Image Files", None, -1))
        self.patternB_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "*LB.TIF", None, -1))
        self.preprocessSettings_GB.setTitle(QtWidgets.QApplication.translate("ImportDialog_Val", "Preprocess Settings", None, -1))
        self.windowSize_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "32", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Search Area Size", None, -1))
        self.searchSize_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "32", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Overlap", None, -1))
        self.overlap_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "16", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Numb. CPU Cores", None, -1))
        self.ncpus_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "2", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Window Size", None, -1))
        self.timeStep_LE.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "0.0015", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "time step", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Signal/Noise Method", None, -1))
        self.sig2noise_CB.setItemText(0, QtWidgets.QApplication.translate("ImportDialog_Val", "peak2peak", None, -1))
        self.sig2noise_CB.setItemText(1, QtWidgets.QApplication.translate("ImportDialog_Val", "peak2mean", None, -1))
        self.sig2noise_CB.setItemText(2, QtWidgets.QApplication.translate("ImportDialog_Val", "None", None, -1))
        self.addFiles_PB.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Add Files", None, -1))
        self.cancel_PB.setText(QtWidgets.QApplication.translate("ImportDialog_Val", "Cancel", None, -1))

