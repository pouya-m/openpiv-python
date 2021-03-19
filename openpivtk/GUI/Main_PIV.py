# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_PIV.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1013, 793)
        MainWindow.setStyleSheet(u"")
        self.actionLoad_Files = QAction(MainWindow)
        self.actionLoad_Files.setObjectName(u"actionLoad_Files")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionClear_Files = QAction(MainWindow)
        self.actionClear_Files.setObjectName(u"actionClear_Files")
        self.actionLoad_Raw_Images = QAction(MainWindow)
        self.actionLoad_Raw_Images.setObjectName(u"actionLoad_Raw_Images")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_11 = QGridLayout(self.centralwidget)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.Main_tabs = QTabWidget(self.centralwidget)
        self.Main_tabs.setObjectName(u"Main_tabs")
        self.Main_tabs.setEnabled(True)
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.Main_tabs.setFont(font)
        self.Main_tabs.setAcceptDrops(False)
        self.Main_tabs.setAutoFillBackground(False)
        self.Main_tabs.setStyleSheet(u"")
        self.Main_tabs.setTabPosition(QTabWidget.North)
        self.Main_tabs.setTabShape(QTabWidget.Rounded)
        self.Main_tabs.setElideMode(Qt.ElideNone)
        self.Main_tabs.setUsesScrollButtons(True)
        self.Main_tabs.setDocumentMode(False)
        self.Main_tabs.setTabsClosable(False)
        self.Main_tabs.setMovable(False)
        self.Main_tabs.setTabBarAutoHide(False)
        self.Validation = QWidget()
        self.Validation.setObjectName(u"Validation")
        self.Validation.setEnabled(True)
        self.gridLayout_4 = QGridLayout(self.Validation)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.Validation)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 10, 5, 5)
        self.settings_GB = QGroupBox(self.layoutWidget)
        self.settings_GB.setObjectName(u"settings_GB")
        self.settings_GB.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.settings_GB.sizePolicy().hasHeightForWidth())
        self.settings_GB.setSizePolicy(sizePolicy1)
        self.settings_GB.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setWeight(50)
        font1.setKerning(True)
        self.settings_GB.setFont(font1)
        self.settings_GB.setAutoFillBackground(False)
        self.settings_GB.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.settings_GB.setFlat(False)
        self.settings_GB.setCheckable(False)
        self.settings_GB.setChecked(False)
        self.gridLayout_5 = QGridLayout(self.settings_GB)
        self.gridLayout_5.setSpacing(9)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(9)
        self.global_velocity_CB = QCheckBox(self.settings_GB)
        self.global_velocity_CB.setObjectName(u"global_velocity_CB")
        self.global_velocity_CB.setEnabled(True)

        self.gridLayout.addWidget(self.global_velocity_CB, 1, 0, 1, 1)

        self.global_uVelocity_LE = QLineEdit(self.settings_GB)
        self.global_uVelocity_LE.setObjectName(u"global_uVelocity_LE")

        self.gridLayout.addWidget(self.global_uVelocity_LE, 1, 1, 1, 1)

        self.global_vVelocity_LE = QLineEdit(self.settings_GB)
        self.global_vVelocity_LE.setObjectName(u"global_vVelocity_LE")

        self.gridLayout.addWidget(self.global_vVelocity_LE, 1, 2, 1, 1)

        self.local_velocity_CB = QCheckBox(self.settings_GB)
        self.local_velocity_CB.setObjectName(u"local_velocity_CB")
        self.local_velocity_CB.setEnabled(True)

        self.gridLayout.addWidget(self.local_velocity_CB, 2, 0, 1, 1)

        self.local_velocity_LE = QLineEdit(self.settings_GB)
        self.local_velocity_LE.setObjectName(u"local_velocity_LE")

        self.gridLayout.addWidget(self.local_velocity_LE, 2, 1, 1, 1)

        self.local_kernel_LE = QLineEdit(self.settings_GB)
        self.local_kernel_LE.setObjectName(u"local_kernel_LE")

        self.gridLayout.addWidget(self.local_kernel_LE, 2, 2, 1, 1)

        self.s2n_CB = QCheckBox(self.settings_GB)
        self.s2n_CB.setObjectName(u"s2n_CB")
        self.s2n_CB.setEnabled(True)

        self.gridLayout.addWidget(self.s2n_CB, 0, 0, 1, 1)

        self.global_std_CB = QCheckBox(self.settings_GB)
        self.global_std_CB.setObjectName(u"global_std_CB")
        self.global_std_CB.setEnabled(True)

        self.gridLayout.addWidget(self.global_std_CB, 3, 0, 1, 2)

        self.s2n_LE = QLineEdit(self.settings_GB)
        self.s2n_LE.setObjectName(u"s2n_LE")
        self.s2n_LE.setEnabled(True)
        self.s2n_LE.setFrame(True)

        self.gridLayout.addWidget(self.s2n_LE, 0, 2, 1, 1)

        self.global_std_LE = QLineEdit(self.settings_GB)
        self.global_std_LE.setObjectName(u"global_std_LE")

        self.gridLayout.addWidget(self.global_std_LE, 3, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.apply_settings_PB = QPushButton(self.settings_GB)
        self.apply_settings_PB.setObjectName(u"apply_settings_PB")

        self.horizontalLayout.addWidget(self.apply_settings_PB)

        self.load_settings_PB = QPushButton(self.settings_GB)
        self.load_settings_PB.setObjectName(u"load_settings_PB")

        self.horizontalLayout.addWidget(self.load_settings_PB)

        self.save_settings_PB = QPushButton(self.settings_GB)
        self.save_settings_PB.setObjectName(u"save_settings_PB")
        self.save_settings_PB.setEnabled(True)

        self.horizontalLayout.addWidget(self.save_settings_PB)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.settings_GB)

        self.files_TW = QTreeWidget(self.layoutWidget)
        self.files_TW.setObjectName(u"files_TW")
        self.files_TW.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.files_TW.sizePolicy().hasHeightForWidth())
        self.files_TW.setSizePolicy(sizePolicy2)
        self.files_TW.setMinimumSize(QSize(0, 0))
        self.files_TW.setAutoScroll(True)
        self.files_TW.setIndentation(0)
        self.files_TW.setItemsExpandable(True)
        self.files_TW.setSortingEnabled(True)
        self.files_TW.setAnimated(True)
        self.files_TW.setAllColumnsShowFocus(False)
        self.files_TW.setWordWrap(False)
        self.files_TW.setHeaderHidden(False)
        self.files_TW.header().setProperty("showSortIndicator", True)

        self.verticalLayout.addWidget(self.files_TW)

        self.splitter.addWidget(self.layoutWidget)
        self.plot_widget = QWidget(self.splitter)
        self.plot_widget.setObjectName(u"plot_widget")
        self.plot_widget.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy3)
        self.plot_widget.setMinimumSize(QSize(450, 0))
        self.plot_widget.setAutoFillBackground(False)
        self.plot_settings_LE = QLineEdit(self.plot_widget)
        self.plot_settings_LE.setObjectName(u"plot_settings_LE")
        self.plot_settings_LE.setGeometry(QRect(160, 30, 70, 30))
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.plot_settings_LE.sizePolicy().hasHeightForWidth())
        self.plot_settings_LE.setSizePolicy(sizePolicy4)
        self.plot_settings_LE.setMinimumSize(QSize(70, 0))
        self.plot_settings_LE.setMaximumSize(QSize(70, 16777215))
        self.BV_settings_CB = QComboBox(self.plot_widget)
        self.BV_settings_CB.addItem("")
        self.BV_settings_CB.addItem("")
        self.BV_settings_CB.addItem("")
        self.BV_settings_CB.addItem("")
        self.BV_settings_CB.setObjectName(u"BV_settings_CB")
        self.BV_settings_CB.setGeometry(QRect(240, 30, 165, 30))
        sizePolicy4.setHeightForWidth(self.BV_settings_CB.sizePolicy().hasHeightForWidth())
        self.BV_settings_CB.setSizePolicy(sizePolicy4)
        self.BV_settings_CB.setMinimumSize(QSize(165, 30))
        self.BV_settings_CB.setMaximumSize(QSize(165, 16777215))
        self.splitter.addWidget(self.plot_widget)

        self.gridLayout_4.addWidget(self.splitter, 0, 0, 1, 1)

        self.Main_tabs.addTab(self.Validation, "")
        self.Process = QWidget()
        self.Process.setObjectName(u"Process")
        self.gridLayout_12 = QGridLayout(self.Process)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setVerticalSpacing(9)
        self.gridLayout_12.setContentsMargins(5, 10, 5, 0)
        self.groupBox_11 = QGroupBox(self.Process)
        self.groupBox_11.setObjectName(u"groupBox_11")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy5)
        self.gridLayout_25 = QGridLayout(self.groupBox_11)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(10, 10, 10, 15)
        self.gridLayout_26 = QGridLayout()
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setHorizontalSpacing(15)
        self.gridLayout_26.setVerticalSpacing(12)
        self.label_21 = QLabel(self.groupBox_11)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_26.addWidget(self.label_21, 0, 0, 1, 1)

        self.label_22 = QLabel(self.groupBox_11)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_26.addWidget(self.label_22, 1, 0, 1, 1)

        self.run_start_PB = QPushButton(self.groupBox_11)
        self.run_start_PB.setObjectName(u"run_start_PB")
        self.run_start_PB.setEnabled(True)
        self.run_start_PB.setStyleSheet(u"")

        self.gridLayout_26.addWidget(self.run_start_PB, 0, 2, 1, 1)

        self.run_stop_PB = QPushButton(self.groupBox_11)
        self.run_stop_PB.setObjectName(u"run_stop_PB")
        self.run_stop_PB.setEnabled(True)

        self.gridLayout_26.addWidget(self.run_stop_PB, 0, 3, 1, 1)

        self.run_overalprogress_PBar = QProgressBar(self.groupBox_11)
        self.run_overalprogress_PBar.setObjectName(u"run_overalprogress_PBar")
        self.run_overalprogress_PBar.setEnabled(False)
        self.run_overalprogress_PBar.setStyleSheet(u"")
        self.run_overalprogress_PBar.setValue(0)
        self.run_overalprogress_PBar.setTextVisible(True)

        self.gridLayout_26.addWidget(self.run_overalprogress_PBar, 2, 1, 1, 3)

        self.run_progress_PBar = QProgressBar(self.groupBox_11)
        self.run_progress_PBar.setObjectName(u"run_progress_PBar")
        self.run_progress_PBar.setEnabled(False)
        self.run_progress_PBar.setStyleSheet(u"")
        self.run_progress_PBar.setValue(0)

        self.gridLayout_26.addWidget(self.run_progress_PBar, 1, 1, 1, 3)

        self.label_23 = QLabel(self.groupBox_11)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_26.addWidget(self.label_23, 2, 0, 1, 1)

        self.run_progress_TE = QPlainTextEdit(self.groupBox_11)
        self.run_progress_TE.setObjectName(u"run_progress_TE")
        sizePolicy5.setHeightForWidth(self.run_progress_TE.sizePolicy().hasHeightForWidth())
        self.run_progress_TE.setSizePolicy(sizePolicy5)
        self.run_progress_TE.setMaximumSize(QSize(16777215, 80))
        self.run_progress_TE.setLayoutDirection(Qt.LeftToRight)
        self.run_progress_TE.setFrameShape(QFrame.StyledPanel)
        self.run_progress_TE.setMidLineWidth(3)
        self.run_progress_TE.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.run_progress_TE.setTabChangesFocus(True)
        self.run_progress_TE.setUndoRedoEnabled(False)
        self.run_progress_TE.setReadOnly(True)
        self.run_progress_TE.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.run_progress_TE.setCenterOnScroll(True)

        self.gridLayout_26.addWidget(self.run_progress_TE, 0, 1, 1, 1)


        self.gridLayout_25.addLayout(self.gridLayout_26, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_11, 1, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.Process)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy2.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy2)
        self.gridLayout_18 = QGridLayout(self.groupBox_7)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setHorizontalSpacing(6)
        self.gridLayout_18.setContentsMargins(10, 10, 10, 10)
        self.horizontalSpacer = QSpacerItem(398, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.process_loadsettings_PB = QPushButton(self.groupBox_7)
        self.process_loadsettings_PB.setObjectName(u"process_loadsettings_PB")

        self.gridLayout_18.addWidget(self.process_loadsettings_PB, 2, 1, 1, 1)

        self.toolBox = QToolBox(self.groupBox_7)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setEnabled(True)
        self.toolBox.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.toolBox.setLayoutDirection(Qt.LeftToRight)
        self.toolBox.setAutoFillBackground(False)
        self.toolBox.setFrameShape(QFrame.NoFrame)
        self.toolBox.setFrameShadow(QFrame.Raised)
        self.ExpPage = QWidget()
        self.ExpPage.setObjectName(u"ExpPage")
        self.ExpPage.setGeometry(QRect(0, 0, 975, 307))
        self.gridLayout_2 = QGridLayout(self.ExpPage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(8, 0, 8, 0)
        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setHorizontalSpacing(10)
        self.gridLayout_13.setVerticalSpacing(8)
        self.label_24 = QLabel(self.ExpPage)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_13.addWidget(self.label_24, 0, 0, 1, 1)

        self.exp_directory_TB = QToolButton(self.ExpPage)
        self.exp_directory_TB.setObjectName(u"exp_directory_TB")

        self.gridLayout_13.addWidget(self.exp_directory_TB, 0, 6, 1, 1)

        self.exp_experiments_LE = QLineEdit(self.ExpPage)
        self.exp_experiments_LE.setObjectName(u"exp_experiments_LE")

        self.gridLayout_13.addWidget(self.exp_experiments_LE, 1, 1, 1, 6)

        self.label_14 = QLabel(self.ExpPage)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_13.addWidget(self.label_14, 2, 0, 1, 1)

        self.exp_runs_LE = QLineEdit(self.ExpPage)
        self.exp_runs_LE.setObjectName(u"exp_runs_LE")

        self.gridLayout_13.addWidget(self.exp_runs_LE, 2, 1, 1, 6)

        self.label_25 = QLabel(self.ExpPage)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_13.addWidget(self.label_25, 1, 0, 1, 1)

        self.exp_directory_LE = QLineEdit(self.ExpPage)
        self.exp_directory_LE.setObjectName(u"exp_directory_LE")

        self.gridLayout_13.addWidget(self.exp_directory_LE, 0, 1, 1, 5)

        self.label = QLabel(self.ExpPage)
        self.label.setObjectName(u"label")

        self.gridLayout_13.addWidget(self.label, 3, 0, 1, 1)

        self.exp_patA_LE = QLineEdit(self.ExpPage)
        self.exp_patA_LE.setObjectName(u"exp_patA_LE")

        self.gridLayout_13.addWidget(self.exp_patA_LE, 3, 1, 1, 1)

        self.label_2 = QLabel(self.ExpPage)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_13.addWidget(self.label_2, 3, 2, 1, 1)

        self.label_3 = QLabel(self.ExpPage)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_13.addWidget(self.label_3, 3, 4, 1, 1)

        self.exp_patB_LE = QLineEdit(self.ExpPage)
        self.exp_patB_LE.setObjectName(u"exp_patB_LE")

        self.gridLayout_13.addWidget(self.exp_patB_LE, 3, 3, 1, 1)

        self.exp_nfiles_LE = QLineEdit(self.ExpPage)
        self.exp_nfiles_LE.setObjectName(u"exp_nfiles_LE")

        self.gridLayout_13.addWidget(self.exp_nfiles_LE, 3, 5, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout_13, 0, 0, 1, 1)

        self.toolBox.addItem(self.ExpPage, u"Experiment")
        self.PrePage = QWidget()
        self.PrePage.setObjectName(u"PrePage")
        self.PrePage.setGeometry(QRect(0, 0, 420, 91))
        self.gridLayout_3 = QGridLayout(self.PrePage)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(8, 0, 8, 0)
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(10)
        self.gridLayout_7.setVerticalSpacing(8)
        self.pre_background_CB = QCheckBox(self.PrePage)
        self.pre_background_CB.setObjectName(u"pre_background_CB")

        self.gridLayout_7.addWidget(self.pre_background_CB, 0, 0, 1, 1)

        self.pre_staticmask_CB = QCheckBox(self.PrePage)
        self.pre_staticmask_CB.setObjectName(u"pre_staticmask_CB")

        self.gridLayout_7.addWidget(self.pre_staticmask_CB, 1, 0, 1, 1)

        self.pre_sm_path_TB = QToolButton(self.PrePage)
        self.pre_sm_path_TB.setObjectName(u"pre_sm_path_TB")

        self.gridLayout_7.addWidget(self.pre_sm_path_TB, 1, 4, 1, 1)

        self.pre_dynamicmask_CB = QCheckBox(self.PrePage)
        self.pre_dynamicmask_CB.setObjectName(u"pre_dynamicmask_CB")

        self.gridLayout_7.addWidget(self.pre_dynamicmask_CB, 2, 0, 1, 3)

        self.pre_sm_path_LE = QLineEdit(self.PrePage)
        self.pre_sm_path_LE.setObjectName(u"pre_sm_path_LE")

        self.gridLayout_7.addWidget(self.pre_sm_path_LE, 1, 1, 1, 3)

        self.pre_bg_nfiles_LE = QLineEdit(self.PrePage)
        self.pre_bg_nfiles_LE.setObjectName(u"pre_bg_nfiles_LE")

        self.gridLayout_7.addWidget(self.pre_bg_nfiles_LE, 0, 1, 1, 3)


        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.toolBox.addItem(self.PrePage, u"Pre-Process")
        self.ProPage = QWidget()
        self.ProPage.setObjectName(u"ProPage")
        self.ProPage.setGeometry(QRect(0, 0, 599, 93))
        self.gridLayout_8 = QGridLayout(self.ProPage)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(8, 0, 8, 0)
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(10)
        self.gridLayout_9.setVerticalSpacing(8)
        self.pro_scale_LE = QLineEdit(self.ProPage)
        self.pro_scale_LE.setObjectName(u"pro_scale_LE")

        self.gridLayout_9.addWidget(self.pro_scale_LE, 1, 6, 1, 1)

        self.pro_searcharea_LE = QLineEdit(self.ProPage)
        self.pro_searcharea_LE.setObjectName(u"pro_searcharea_LE")

        self.gridLayout_9.addWidget(self.pro_searcharea_LE, 0, 4, 1, 1)

        self.label_8 = QLabel(self.ProPage)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_9.addWidget(self.label_8, 2, 0, 1, 2)

        self.label_7 = QLabel(self.ProPage)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_9.addWidget(self.label_7, 0, 5, 1, 1)

        self.label_10 = QLabel(self.ProPage)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_9.addWidget(self.label_10, 1, 3, 1, 1)

        self.label_12 = QLabel(self.ProPage)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_9.addWidget(self.label_12, 1, 5, 1, 1)

        self.label_11 = QLabel(self.ProPage)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_9.addWidget(self.label_11, 1, 0, 1, 2)

        self.pro_sig2noise_CB = QComboBox(self.ProPage)
        self.pro_sig2noise_CB.addItem("")
        self.pro_sig2noise_CB.addItem("")
        self.pro_sig2noise_CB.addItem("")
        self.pro_sig2noise_CB.setObjectName(u"pro_sig2noise_CB")

        self.gridLayout_9.addWidget(self.pro_sig2noise_CB, 1, 2, 1, 1)

        self.pro_timestep_LE = QLineEdit(self.ProPage)
        self.pro_timestep_LE.setObjectName(u"pro_timestep_LE")

        self.gridLayout_9.addWidget(self.pro_timestep_LE, 1, 4, 1, 1)

        self.pro_ncpus_LE = QLineEdit(self.ProPage)
        self.pro_ncpus_LE.setObjectName(u"pro_ncpus_LE")

        self.gridLayout_9.addWidget(self.pro_ncpus_LE, 2, 2, 1, 1)

        self.pro_overlap_LE = QLineEdit(self.ProPage)
        self.pro_overlap_LE.setObjectName(u"pro_overlap_LE")

        self.gridLayout_9.addWidget(self.pro_overlap_LE, 0, 6, 1, 1)

        self.label_4 = QLabel(self.ProPage)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_9.addWidget(self.label_4, 0, 3, 1, 1)

        self.label_9 = QLabel(self.ProPage)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_9.addWidget(self.label_9, 0, 0, 1, 2)

        self.pro_windowsize_LE = QLineEdit(self.ProPage)
        self.pro_windowsize_LE.setObjectName(u"pro_windowsize_LE")

        self.gridLayout_9.addWidget(self.pro_windowsize_LE, 0, 2, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_9, 0, 0, 1, 1)

        self.toolBox.addItem(self.ProPage, u"Process")
        self.PosPage = QWidget()
        self.PosPage.setObjectName(u"PosPage")
        self.PosPage.setGeometry(QRect(0, 0, 560, 288))
        self.gridLayout_10 = QGridLayout(self.PosPage)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.groupBox_9 = QGroupBox(self.PosPage)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_21 = QGridLayout(self.groupBox_9)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(8, 10, 8, 5)
        self.gridLayout_22 = QGridLayout()
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.pos_std_LE = QLineEdit(self.groupBox_9)
        self.pos_std_LE.setObjectName(u"pos_std_LE")

        self.gridLayout_22.addWidget(self.pos_std_LE, 1, 1, 1, 1)

        self.pos_s2n_ratio_LE = QLineEdit(self.groupBox_9)
        self.pos_s2n_ratio_LE.setObjectName(u"pos_s2n_ratio_LE")
        self.pos_s2n_ratio_LE.setEnabled(True)
        self.pos_s2n_ratio_LE.setFrame(True)

        self.gridLayout_22.addWidget(self.pos_s2n_ratio_LE, 0, 1, 1, 1)

        self.pos_gv_ulim_LE = QLineEdit(self.groupBox_9)
        self.pos_gv_ulim_LE.setObjectName(u"pos_gv_ulim_LE")

        self.gridLayout_22.addWidget(self.pos_gv_ulim_LE, 0, 3, 1, 1)

        self.pos_std_CB = QCheckBox(self.groupBox_9)
        self.pos_std_CB.setObjectName(u"pos_std_CB")
        self.pos_std_CB.setEnabled(True)

        self.gridLayout_22.addWidget(self.pos_std_CB, 1, 0, 1, 1)

        self.pos_localvelocity_CB = QCheckBox(self.groupBox_9)
        self.pos_localvelocity_CB.setObjectName(u"pos_localvelocity_CB")
        self.pos_localvelocity_CB.setEnabled(True)

        self.gridLayout_22.addWidget(self.pos_localvelocity_CB, 1, 2, 1, 1)

        self.pos_lv_uvdiff_LE = QLineEdit(self.groupBox_9)
        self.pos_lv_uvdiff_LE.setObjectName(u"pos_lv_uvdiff_LE")

        self.gridLayout_22.addWidget(self.pos_lv_uvdiff_LE, 1, 3, 1, 1)

        self.pos_sig2noise_CB = QCheckBox(self.groupBox_9)
        self.pos_sig2noise_CB.setObjectName(u"pos_sig2noise_CB")
        self.pos_sig2noise_CB.setEnabled(True)

        self.gridLayout_22.addWidget(self.pos_sig2noise_CB, 0, 0, 1, 1)

        self.pos_globalvelocity_CB = QCheckBox(self.groupBox_9)
        self.pos_globalvelocity_CB.setObjectName(u"pos_globalvelocity_CB")
        self.pos_globalvelocity_CB.setEnabled(True)

        self.gridLayout_22.addWidget(self.pos_globalvelocity_CB, 0, 2, 1, 1)

        self.pos_lv_kernel_LE = QLineEdit(self.groupBox_9)
        self.pos_lv_kernel_LE.setObjectName(u"pos_lv_kernel_LE")

        self.gridLayout_22.addWidget(self.pos_lv_kernel_LE, 1, 4, 1, 1)

        self.pos_gv_vlim_LE = QLineEdit(self.groupBox_9)
        self.pos_gv_vlim_LE.setObjectName(u"pos_gv_vlim_LE")

        self.gridLayout_22.addWidget(self.pos_gv_vlim_LE, 0, 4, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout_22, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_9, 0, 0, 1, 1)

        self.groupBox_10 = QGroupBox(self.PosPage)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_14 = QGridLayout(self.groupBox_10)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(9, -1, -1, -1)
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.pos_badvector_CB = QCheckBox(self.groupBox_10)
        self.pos_badvector_CB.setObjectName(u"pos_badvector_CB")
        self.pos_badvector_CB.setEnabled(True)

        self.gridLayout_6.addWidget(self.pos_badvector_CB, 0, 0, 1, 2)

        self.pos_bv_niterations_LE = QLineEdit(self.groupBox_10)
        self.pos_bv_niterations_LE.setObjectName(u"pos_bv_niterations_LE")

        self.gridLayout_6.addWidget(self.pos_bv_niterations_LE, 0, 3, 1, 1)

        self.pos_bv_method_CB = QComboBox(self.groupBox_10)
        self.pos_bv_method_CB.addItem("")
        self.pos_bv_method_CB.addItem("")
        self.pos_bv_method_CB.addItem("")
        self.pos_bv_method_CB.setObjectName(u"pos_bv_method_CB")
        sizePolicy5.setHeightForWidth(self.pos_bv_method_CB.sizePolicy().hasHeightForWidth())
        self.pos_bv_method_CB.setSizePolicy(sizePolicy5)

        self.gridLayout_6.addWidget(self.pos_bv_method_CB, 0, 2, 1, 1)

        self.pos_bv_kernel_LE = QLineEdit(self.groupBox_10)
        self.pos_bv_kernel_LE.setObjectName(u"pos_bv_kernel_LE")

        self.gridLayout_6.addWidget(self.pos_bv_kernel_LE, 0, 4, 1, 1)

        self.pos_smth_factor_LE = QLineEdit(self.groupBox_10)
        self.pos_smth_factor_LE.setObjectName(u"pos_smth_factor_LE")

        self.gridLayout_6.addWidget(self.pos_smth_factor_LE, 1, 2, 1, 1)

        self.pos_smoothing_CB = QCheckBox(self.groupBox_10)
        self.pos_smoothing_CB.setObjectName(u"pos_smoothing_CB")
        self.pos_smoothing_CB.setEnabled(True)
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pos_smoothing_CB.sizePolicy().hasHeightForWidth())
        self.pos_smoothing_CB.setSizePolicy(sizePolicy6)

        self.gridLayout_6.addWidget(self.pos_smoothing_CB, 1, 0, 1, 2)

        self.pos_fm_LE = QLineEdit(self.groupBox_10)
        self.pos_fm_LE.setObjectName(u"pos_fm_LE")

        self.gridLayout_6.addWidget(self.pos_fm_LE, 2, 2, 1, 1)

        self.pos_fieldmanip_CB = QCheckBox(self.groupBox_10)
        self.pos_fieldmanip_CB.setObjectName(u"pos_fieldmanip_CB")
        self.pos_fieldmanip_CB.setEnabled(True)

        self.gridLayout_6.addWidget(self.pos_fieldmanip_CB, 2, 0, 1, 2)


        self.gridLayout_14.addLayout(self.gridLayout_6, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_10, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(5, 10, 25, -1)
        self.label_15 = QLabel(self.PosPage)
        self.label_15.setObjectName(u"label_15")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy7)
        self.label_15.setMinimumSize(QSize(150, 0))
        self.label_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_15)

        self.pos_output_CB = QComboBox(self.PosPage)
        self.pos_output_CB.addItem("")
        self.pos_output_CB.addItem("")
        self.pos_output_CB.setObjectName(u"pos_output_CB")

        self.horizontalLayout_3.addWidget(self.pos_output_CB)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 2)

        self.gridLayout_10.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        self.toolBox.addItem(self.PosPage, u"Post-Process")

        self.gridLayout_18.addWidget(self.toolBox, 0, 0, 1, 3)

        self.process_savesettings_PB = QPushButton(self.groupBox_7)
        self.process_savesettings_PB.setObjectName(u"process_savesettings_PB")

        self.gridLayout_18.addWidget(self.process_savesettings_PB, 2, 2, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_7, 0, 0, 1, 1)

        self.Main_tabs.addTab(self.Process, "")
        self.FrequencyAnalysis = QWidget()
        self.FrequencyAnalysis.setObjectName(u"FrequencyAnalysis")
        self.verticalLayout_3 = QVBoxLayout(self.FrequencyAnalysis)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.freq_exp_GB = QGroupBox(self.FrequencyAnalysis)
        self.freq_exp_GB.setObjectName(u"freq_exp_GB")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(2)
        sizePolicy8.setVerticalStretch(2)
        sizePolicy8.setHeightForWidth(self.freq_exp_GB.sizePolicy().hasHeightForWidth())
        self.freq_exp_GB.setSizePolicy(sizePolicy8)
        self.gridLayout_23 = QGridLayout(self.freq_exp_GB)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setHorizontalSpacing(20)
        self.gridLayout_23.setVerticalSpacing(5)
        self.label_30 = QLabel(self.freq_exp_GB)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_23.addWidget(self.label_30, 1, 0, 1, 1)

        self.label_31 = QLabel(self.freq_exp_GB)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_23.addWidget(self.label_31, 2, 0, 1, 1)

        self.freq_exp_LE = QLineEdit(self.freq_exp_GB)
        self.freq_exp_LE.setObjectName(u"freq_exp_LE")

        self.gridLayout_23.addWidget(self.freq_exp_LE, 2, 1, 1, 1)

        self.label_32 = QLabel(self.freq_exp_GB)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_23.addWidget(self.label_32, 2, 2, 1, 1)

        self.label_13 = QLabel(self.freq_exp_GB)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_23.addWidget(self.label_13, 3, 0, 1, 1)

        self.freq_pat_LE = QLineEdit(self.freq_exp_GB)
        self.freq_pat_LE.setObjectName(u"freq_pat_LE")

        self.gridLayout_23.addWidget(self.freq_pat_LE, 3, 1, 1, 1)

        self.label_33 = QLabel(self.freq_exp_GB)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_23.addWidget(self.label_33, 3, 2, 1, 1)

        self.freq_dir_LE = QLineEdit(self.freq_exp_GB)
        self.freq_dir_LE.setObjectName(u"freq_dir_LE")

        self.gridLayout_23.addWidget(self.freq_dir_LE, 1, 1, 1, 1)

        self.freq_dir_TB = QToolButton(self.freq_exp_GB)
        self.freq_dir_TB.setObjectName(u"freq_dir_TB")

        self.gridLayout_23.addWidget(self.freq_dir_TB, 1, 2, 1, 1)

        self.freq_nf_LE = QLineEdit(self.freq_exp_GB)
        self.freq_nf_LE.setObjectName(u"freq_nf_LE")

        self.gridLayout_23.addWidget(self.freq_nf_LE, 3, 3, 1, 1)

        self.freq_run_LE = QLineEdit(self.freq_exp_GB)
        self.freq_run_LE.setObjectName(u"freq_run_LE")

        self.gridLayout_23.addWidget(self.freq_run_LE, 2, 3, 1, 1)

        self.freq_load_from_PB = QPushButton(self.freq_exp_GB)
        self.freq_load_from_PB.setObjectName(u"freq_load_from_PB")

        self.gridLayout_23.addWidget(self.freq_load_from_PB, 0, 0, 1, 4)


        self.verticalLayout_3.addWidget(self.freq_exp_GB)

        self.freq_analysis_GB = QGroupBox(self.FrequencyAnalysis)
        self.freq_analysis_GB.setObjectName(u"freq_analysis_GB")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(3)
        sizePolicy9.setVerticalStretch(3)
        sizePolicy9.setHeightForWidth(self.freq_analysis_GB.sizePolicy().hasHeightForWidth())
        self.freq_analysis_GB.setSizePolicy(sizePolicy9)
        self.gridLayout_29 = QGridLayout(self.freq_analysis_GB)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.gridLayout_29.setContentsMargins(-1, -1, -1, 2)
        self.label_36 = QLabel(self.freq_analysis_GB)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_29.addWidget(self.label_36, 0, 0, 1, 1)

        self.freq_fs_LE = QLineEdit(self.freq_analysis_GB)
        self.freq_fs_LE.setObjectName(u"freq_fs_LE")

        self.gridLayout_29.addWidget(self.freq_fs_LE, 0, 1, 1, 2)

        self.label_37 = QLabel(self.freq_analysis_GB)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_29.addWidget(self.label_37, 0, 3, 1, 1)

        self.freq_dim_LE = QLineEdit(self.freq_analysis_GB)
        self.freq_dim_LE.setObjectName(u"freq_dim_LE")

        self.gridLayout_29.addWidget(self.freq_dim_LE, 0, 4, 1, 1)

        self.label_38 = QLabel(self.freq_analysis_GB)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_29.addWidget(self.label_38, 0, 5, 1, 1)

        self.freq_flim_LE = QLineEdit(self.freq_analysis_GB)
        self.freq_flim_LE.setObjectName(u"freq_flim_LE")

        self.gridLayout_29.addWidget(self.freq_flim_LE, 0, 6, 1, 1)

        self.freq_pt_fft_CB = QCheckBox(self.freq_analysis_GB)
        self.freq_pt_fft_CB.setObjectName(u"freq_pt_fft_CB")

        self.gridLayout_29.addWidget(self.freq_pt_fft_CB, 1, 0, 1, 1)

        self.freq_pt_stft_CB = QCheckBox(self.freq_analysis_GB)
        self.freq_pt_stft_CB.setObjectName(u"freq_pt_stft_CB")

        self.gridLayout_29.addWidget(self.freq_pt_stft_CB, 2, 0, 1, 1)

        self.freq_gb_fft_CB = QCheckBox(self.freq_analysis_GB)
        self.freq_gb_fft_CB.setObjectName(u"freq_gb_fft_CB")

        self.gridLayout_29.addWidget(self.freq_gb_fft_CB, 3, 0, 1, 1)

        self.freq_gb_stft_CB = QCheckBox(self.freq_analysis_GB)
        self.freq_gb_stft_CB.setObjectName(u"freq_gb_stft_CB")

        self.gridLayout_29.addWidget(self.freq_gb_stft_CB, 4, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.freq_analysis_GB)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_31 = QGridLayout(self.groupBox_3)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setContentsMargins(-1, 10, -1, 2)
        self.label_39 = QLabel(self.groupBox_3)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_31.addWidget(self.label_39, 0, 0, 1, 1)

        self.label_40 = QLabel(self.groupBox_3)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_31.addWidget(self.label_40, 0, 2, 1, 1)

        self.freq_noverlap_LE = QLineEdit(self.groupBox_3)
        self.freq_noverlap_LE.setObjectName(u"freq_noverlap_LE")

        self.gridLayout_31.addWidget(self.freq_noverlap_LE, 0, 3, 1, 1)

        self.freq_nperseg_LE = QLineEdit(self.groupBox_3)
        self.freq_nperseg_LE.setObjectName(u"freq_nperseg_LE")

        self.gridLayout_31.addWidget(self.freq_nperseg_LE, 0, 1, 1, 1)


        self.gridLayout_29.addWidget(self.groupBox_3, 3, 1, 2, 6)

        self.groupBox_2 = QGroupBox(self.freq_analysis_GB)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_30 = QGridLayout(self.groupBox_2)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(-1, 10, -1, 2)
        self.label_41 = QLabel(self.groupBox_2)
        self.label_41.setObjectName(u"label_41")
        sizePolicy1.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy1)

        self.gridLayout_30.addWidget(self.label_41, 0, 0, 1, 1)

        self.freq_pt_loc_CB = QComboBox(self.groupBox_2)
        self.freq_pt_loc_CB.addItem("")
        self.freq_pt_loc_CB.addItem("")
        self.freq_pt_loc_CB.addItem("")
        self.freq_pt_loc_CB.setObjectName(u"freq_pt_loc_CB")
        sizePolicy5.setHeightForWidth(self.freq_pt_loc_CB.sizePolicy().hasHeightForWidth())
        self.freq_pt_loc_CB.setSizePolicy(sizePolicy5)

        self.gridLayout_30.addWidget(self.freq_pt_loc_CB, 0, 1, 1, 1)

        self.freq_pt_loc_LE = QLineEdit(self.groupBox_2)
        self.freq_pt_loc_LE.setObjectName(u"freq_pt_loc_LE")
        sizePolicy5.setHeightForWidth(self.freq_pt_loc_LE.sizePolicy().hasHeightForWidth())
        self.freq_pt_loc_LE.setSizePolicy(sizePolicy5)

        self.gridLayout_30.addWidget(self.freq_pt_loc_LE, 0, 2, 1, 1)


        self.gridLayout_29.addWidget(self.groupBox_2, 1, 1, 2, 6)


        self.verticalLayout_3.addWidget(self.freq_analysis_GB)

        self.frame = QFrame(self.FrequencyAnalysis)
        self.frame.setObjectName(u"frame")
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_32 = QGridLayout(self.frame)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(590, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_32.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.freq_load_PB = QPushButton(self.frame)
        self.freq_load_PB.setObjectName(u"freq_load_PB")

        self.gridLayout_32.addWidget(self.freq_load_PB, 0, 1, 1, 1)

        self.freq_save_PB = QPushButton(self.frame)
        self.freq_save_PB.setObjectName(u"freq_save_PB")

        self.gridLayout_32.addWidget(self.freq_save_PB, 0, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.frame)

        self.freq_run_GB = QGroupBox(self.FrequencyAnalysis)
        self.freq_run_GB.setObjectName(u"freq_run_GB")
        sizePolicy8.setHeightForWidth(self.freq_run_GB.sizePolicy().hasHeightForWidth())
        self.freq_run_GB.setSizePolicy(sizePolicy8)
        self.gridLayout_24 = QGridLayout(self.freq_run_GB)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_28 = QGridLayout()
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_28.setHorizontalSpacing(15)
        self.gridLayout_28.setVerticalSpacing(12)
        self.label_34 = QLabel(self.freq_run_GB)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_28.addWidget(self.label_34, 1, 0, 1, 1)

        self.freq_start_PB = QPushButton(self.freq_run_GB)
        self.freq_start_PB.setObjectName(u"freq_start_PB")
        self.freq_start_PB.setEnabled(True)
        self.freq_start_PB.setStyleSheet(u"")

        self.gridLayout_28.addWidget(self.freq_start_PB, 0, 2, 1, 1)

        self.freq_stop_PB = QPushButton(self.freq_run_GB)
        self.freq_stop_PB.setObjectName(u"freq_stop_PB")
        self.freq_stop_PB.setEnabled(True)

        self.gridLayout_28.addWidget(self.freq_stop_PB, 0, 3, 1, 1)

        self.freq_progress_PBar = QProgressBar(self.freq_run_GB)
        self.freq_progress_PBar.setObjectName(u"freq_progress_PBar")
        self.freq_progress_PBar.setEnabled(False)
        self.freq_progress_PBar.setStyleSheet(u"")
        self.freq_progress_PBar.setValue(0)

        self.gridLayout_28.addWidget(self.freq_progress_PBar, 1, 1, 1, 3)

        self.label_35 = QLabel(self.freq_run_GB)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_28.addWidget(self.label_35, 0, 0, 1, 1)

        self.freq_progress_TE = QPlainTextEdit(self.freq_run_GB)
        self.freq_progress_TE.setObjectName(u"freq_progress_TE")
        sizePolicy5.setHeightForWidth(self.freq_progress_TE.sizePolicy().hasHeightForWidth())
        self.freq_progress_TE.setSizePolicy(sizePolicy5)
        self.freq_progress_TE.setMaximumSize(QSize(16777215, 80))
        self.freq_progress_TE.setLayoutDirection(Qt.LeftToRight)
        self.freq_progress_TE.setFrameShape(QFrame.StyledPanel)
        self.freq_progress_TE.setMidLineWidth(3)
        self.freq_progress_TE.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.freq_progress_TE.setTabChangesFocus(True)
        self.freq_progress_TE.setUndoRedoEnabled(False)
        self.freq_progress_TE.setReadOnly(True)
        self.freq_progress_TE.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.freq_progress_TE.setCenterOnScroll(True)

        self.gridLayout_28.addWidget(self.freq_progress_TE, 0, 1, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout_28, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.freq_run_GB)

        self.Main_tabs.addTab(self.FrequencyAnalysis, "")
        self.ModalAnalysis = QWidget()
        self.ModalAnalysis.setObjectName(u"ModalAnalysis")
        self.gridLayout_15 = QGridLayout(self.ModalAnalysis)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.modal_ana_GB = QGroupBox(self.ModalAnalysis)
        self.modal_ana_GB.setObjectName(u"modal_ana_GB")
        self.gridLayout_17 = QGridLayout(self.modal_ana_GB)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label_5 = QLabel(self.modal_ana_GB)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_17.addWidget(self.label_5, 0, 0, 1, 2)

        self.horizontalSpacer_5 = QSpacerItem(662, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)

        self.mdl_analysis_SW = QStackedWidget(self.modal_ana_GB)
        self.mdl_analysis_SW.setObjectName(u"mdl_analysis_SW")
        self.mdl_analysis_SW.setEnabled(True)
        self.page0 = QWidget()
        self.page0.setObjectName(u"page0")
        self.gridLayout_19 = QGridLayout(self.page0)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.horizontalSpacer_7 = QSpacerItem(84, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_7, 0, 1, 1, 1)

        self.label_18 = QLabel(self.page0)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_19.addWidget(self.label_18, 0, 2, 1, 1)

        self.mdl_rec_CB = QCheckBox(self.page0)
        self.mdl_rec_CB.setObjectName(u"mdl_rec_CB")

        self.gridLayout_19.addWidget(self.mdl_rec_CB, 1, 0, 1, 1)

        self.mdl_rec_nm_LE = QLineEdit(self.page0)
        self.mdl_rec_nm_LE.setObjectName(u"mdl_rec_nm_LE")

        self.gridLayout_19.addWidget(self.mdl_rec_nm_LE, 1, 3, 1, 1)

        self.mdl_nm_LE = QLineEdit(self.page0)
        self.mdl_nm_LE.setObjectName(u"mdl_nm_LE")

        self.gridLayout_19.addWidget(self.mdl_nm_LE, 0, 3, 1, 1)

        self.mdl_rec_ns_LE = QLineEdit(self.page0)
        self.mdl_rec_ns_LE.setObjectName(u"mdl_rec_ns_LE")

        self.gridLayout_19.addWidget(self.mdl_rec_ns_LE, 1, 5, 1, 1)

        self.label_20 = QLabel(self.page0)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_19.addWidget(self.label_20, 1, 4, 1, 1)

        self.label_19 = QLabel(self.page0)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_19.addWidget(self.label_19, 1, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(390, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_6, 0, 4, 1, 2)

        self.horizontalSpacer_8 = QSpacerItem(84, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_8, 1, 1, 1, 1)

        self.mdl_st_CB = QCheckBox(self.page0)
        self.mdl_st_CB.setObjectName(u"mdl_st_CB")

        self.gridLayout_19.addWidget(self.mdl_st_CB, 0, 0, 1, 1)

        self.mdl_analysis_SW.addWidget(self.page0)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.gridLayout_33 = QGridLayout(self.page1)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.mdl_spod_st_CB = QCheckBox(self.page1)
        self.mdl_spod_st_CB.setObjectName(u"mdl_spod_st_CB")

        self.gridLayout_33.addWidget(self.mdl_spod_st_CB, 0, 0, 1, 1)

        self.label_42 = QLabel(self.page1)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_33.addWidget(self.label_42, 1, 0, 1, 1)

        self.mdl_spod_nperseg_LE = QLineEdit(self.page1)
        self.mdl_spod_nperseg_LE.setObjectName(u"mdl_spod_nperseg_LE")

        self.gridLayout_33.addWidget(self.mdl_spod_nperseg_LE, 1, 1, 1, 1)

        self.label_43 = QLabel(self.page1)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_33.addWidget(self.label_43, 1, 2, 1, 2)

        self.mdl_spod_ol_LE = QLineEdit(self.page1)
        self.mdl_spod_ol_LE.setObjectName(u"mdl_spod_ol_LE")

        self.gridLayout_33.addWidget(self.mdl_spod_ol_LE, 1, 4, 1, 1)

        self.label_44 = QLabel(self.page1)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_33.addWidget(self.label_44, 1, 5, 1, 1)

        self.mdl_spod_win_LE = QLineEdit(self.page1)
        self.mdl_spod_win_LE.setObjectName(u"mdl_spod_win_LE")

        self.gridLayout_33.addWidget(self.mdl_spod_win_LE, 1, 6, 1, 1)

        self.label_45 = QLabel(self.page1)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_33.addWidget(self.label_45, 2, 0, 1, 1)

        self.mdl_spod_fs_LE = QLineEdit(self.page1)
        self.mdl_spod_fs_LE.setObjectName(u"mdl_spod_fs_LE")

        self.gridLayout_33.addWidget(self.mdl_spod_fs_LE, 2, 1, 1, 1)

        self.label_46 = QLabel(self.page1)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_33.addWidget(self.label_46, 2, 2, 1, 2)

        self.mdl_spod_fdim_LE = QLineEdit(self.page1)
        self.mdl_spod_fdim_LE.setObjectName(u"mdl_spod_fdim_LE")

        self.gridLayout_33.addWidget(self.mdl_spod_fdim_LE, 2, 4, 1, 1)

        self.label_47 = QLabel(self.page1)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_33.addWidget(self.label_47, 2, 5, 1, 1)

        self.mdl_spod_flim_LE = QLineEdit(self.page1)
        self.mdl_spod_flim_LE.setObjectName(u"mdl_spod_flim_LE")

        self.gridLayout_33.addWidget(self.mdl_spod_flim_LE, 2, 6, 1, 1)

        self.mdl_ffield_st_CB = QCheckBox(self.page1)
        self.mdl_ffield_st_CB.setObjectName(u"mdl_ffield_st_CB")

        self.gridLayout_33.addWidget(self.mdl_ffield_st_CB, 3, 0, 1, 2)

        self.label_49 = QLabel(self.page1)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_33.addWidget(self.label_49, 3, 2, 1, 1)

        self.label_48 = QLabel(self.page1)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_33.addWidget(self.label_48, 3, 5, 1, 1)

        self.mdl_ffield_fd_LE = QLineEdit(self.page1)
        self.mdl_ffield_fd_LE.setObjectName(u"mdl_ffield_fd_LE")

        self.gridLayout_33.addWidget(self.mdl_ffield_fd_LE, 3, 6, 1, 1)

        self.mdl_ffield_mt_CB = QComboBox(self.page1)
        self.mdl_ffield_mt_CB.addItem("")
        self.mdl_ffield_mt_CB.addItem("")
        self.mdl_ffield_mt_CB.setObjectName(u"mdl_ffield_mt_CB")

        self.gridLayout_33.addWidget(self.mdl_ffield_mt_CB, 3, 4, 1, 1)

        self.mdl_analysis_SW.addWidget(self.page1)

        self.gridLayout_17.addWidget(self.mdl_analysis_SW, 1, 0, 2, 4)

        self.mdl_method_CB = QComboBox(self.modal_ana_GB)
        self.mdl_method_CB.addItem("")
        self.mdl_method_CB.addItem("")
        self.mdl_method_CB.addItem("")
        self.mdl_method_CB.setObjectName(u"mdl_method_CB")

        self.gridLayout_17.addWidget(self.mdl_method_CB, 0, 2, 1, 1)


        self.horizontalLayout_2.addWidget(self.modal_ana_GB, 0, Qt.AlignVCenter)


        self.gridLayout_15.addLayout(self.horizontalLayout_2, 1, 0, 1, 4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.mdl_save_PB = QPushButton(self.ModalAnalysis)
        self.mdl_save_PB.setObjectName(u"mdl_save_PB")

        self.gridLayout_15.addWidget(self.mdl_save_PB, 2, 2, 1, 1)

        self.mdl_load_PB = QPushButton(self.ModalAnalysis)
        self.mdl_load_PB.setObjectName(u"mdl_load_PB")

        self.gridLayout_15.addWidget(self.mdl_load_PB, 2, 1, 1, 1)

        self.modal_run_GB = QGroupBox(self.ModalAnalysis)
        self.modal_run_GB.setObjectName(u"modal_run_GB")
        self.gridLayout_20 = QGridLayout(self.modal_run_GB)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setHorizontalSpacing(15)
        self.gridLayout_27.setVerticalSpacing(12)
        self.label_29 = QLabel(self.modal_run_GB)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_27.addWidget(self.label_29, 1, 0, 1, 1)

        self.mdl_start_PB = QPushButton(self.modal_run_GB)
        self.mdl_start_PB.setObjectName(u"mdl_start_PB")
        self.mdl_start_PB.setEnabled(True)
        self.mdl_start_PB.setStyleSheet(u"")

        self.gridLayout_27.addWidget(self.mdl_start_PB, 0, 2, 1, 1)

        self.mdl_stop_PB = QPushButton(self.modal_run_GB)
        self.mdl_stop_PB.setObjectName(u"mdl_stop_PB")
        self.mdl_stop_PB.setEnabled(True)

        self.gridLayout_27.addWidget(self.mdl_stop_PB, 0, 3, 1, 1)

        self.mdl_progress_PBar = QProgressBar(self.modal_run_GB)
        self.mdl_progress_PBar.setObjectName(u"mdl_progress_PBar")
        self.mdl_progress_PBar.setEnabled(False)
        self.mdl_progress_PBar.setStyleSheet(u"")
        self.mdl_progress_PBar.setValue(0)

        self.gridLayout_27.addWidget(self.mdl_progress_PBar, 1, 1, 1, 3)

        self.label_28 = QLabel(self.modal_run_GB)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_27.addWidget(self.label_28, 0, 0, 1, 1)

        self.mdl_progress_TE = QPlainTextEdit(self.modal_run_GB)
        self.mdl_progress_TE.setObjectName(u"mdl_progress_TE")
        sizePolicy5.setHeightForWidth(self.mdl_progress_TE.sizePolicy().hasHeightForWidth())
        self.mdl_progress_TE.setSizePolicy(sizePolicy5)
        self.mdl_progress_TE.setMaximumSize(QSize(16777215, 80))
        self.mdl_progress_TE.setLayoutDirection(Qt.LeftToRight)
        self.mdl_progress_TE.setFrameShape(QFrame.StyledPanel)
        self.mdl_progress_TE.setMidLineWidth(3)
        self.mdl_progress_TE.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdl_progress_TE.setTabChangesFocus(True)
        self.mdl_progress_TE.setUndoRedoEnabled(False)
        self.mdl_progress_TE.setReadOnly(True)
        self.mdl_progress_TE.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.mdl_progress_TE.setCenterOnScroll(True)

        self.gridLayout_27.addWidget(self.mdl_progress_TE, 0, 1, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_27, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.modal_run_GB, 3, 0, 1, 4)

        self.modal_exp_GB = QGroupBox(self.ModalAnalysis)
        self.modal_exp_GB.setObjectName(u"modal_exp_GB")
        self.gridLayout_16 = QGridLayout(self.modal_exp_GB)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setHorizontalSpacing(20)
        self.gridLayout_16.setVerticalSpacing(5)
        self.label_26 = QLabel(self.modal_exp_GB)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_16.addWidget(self.label_26, 1, 0, 1, 1)

        self.label_27 = QLabel(self.modal_exp_GB)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_16.addWidget(self.label_27, 2, 0, 1, 1)

        self.mdl_exp_LE = QLineEdit(self.modal_exp_GB)
        self.mdl_exp_LE.setObjectName(u"mdl_exp_LE")

        self.gridLayout_16.addWidget(self.mdl_exp_LE, 2, 1, 1, 1)

        self.label_16 = QLabel(self.modal_exp_GB)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_16.addWidget(self.label_16, 2, 2, 1, 1)

        self.label_6 = QLabel(self.modal_exp_GB)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_16.addWidget(self.label_6, 3, 0, 1, 1)

        self.mdl_pat_LE = QLineEdit(self.modal_exp_GB)
        self.mdl_pat_LE.setObjectName(u"mdl_pat_LE")

        self.gridLayout_16.addWidget(self.mdl_pat_LE, 3, 1, 1, 1)

        self.label_17 = QLabel(self.modal_exp_GB)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_16.addWidget(self.label_17, 3, 2, 1, 1)

        self.mdl_dir_LE = QLineEdit(self.modal_exp_GB)
        self.mdl_dir_LE.setObjectName(u"mdl_dir_LE")

        self.gridLayout_16.addWidget(self.mdl_dir_LE, 1, 1, 1, 1)

        self.mdl_dir_TB = QToolButton(self.modal_exp_GB)
        self.mdl_dir_TB.setObjectName(u"mdl_dir_TB")

        self.gridLayout_16.addWidget(self.mdl_dir_TB, 1, 2, 1, 1)

        self.mdl_nf_LE = QLineEdit(self.modal_exp_GB)
        self.mdl_nf_LE.setObjectName(u"mdl_nf_LE")

        self.gridLayout_16.addWidget(self.mdl_nf_LE, 3, 3, 1, 1)

        self.mdl_run_LE = QLineEdit(self.modal_exp_GB)
        self.mdl_run_LE.setObjectName(u"mdl_run_LE")

        self.gridLayout_16.addWidget(self.mdl_run_LE, 2, 3, 1, 1)

        self.mdl_load_from_PB = QPushButton(self.modal_exp_GB)
        self.mdl_load_from_PB.setObjectName(u"mdl_load_from_PB")

        self.gridLayout_16.addWidget(self.mdl_load_from_PB, 0, 0, 1, 4)


        self.gridLayout_15.addWidget(self.modal_exp_GB, 0, 0, 1, 4)

        self.Main_tabs.addTab(self.ModalAnalysis, "")

        self.gridLayout_11.addWidget(self.Main_tabs, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1013, 31))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionLoad_Files)
        self.menuFile.addAction(self.actionClear_Files)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.Main_tabs.setCurrentIndex(3)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(4)
        self.mdl_analysis_SW.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.actionLoad_Files.setText(QCoreApplication.translate("MainWindow", u"Load Files", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionClear_Files.setText(QCoreApplication.translate("MainWindow", u"Clear Files", None))
        self.actionLoad_Raw_Images.setText(QCoreApplication.translate("MainWindow", u"Load Raw Images", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
#if QT_CONFIG(accessibility)
        self.Main_tabs.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.settings_GB.setTitle(QCoreApplication.translate("MainWindow", u"Thresholding Settings", None))
        self.global_velocity_CB.setText(QCoreApplication.translate("MainWindow", u"Global Velocity", None))
        self.global_uVelocity_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Umin, Umax", None))
        self.global_vVelocity_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Vmin, Vmax", None))
        self.local_velocity_CB.setText(QCoreApplication.translate("MainWindow", u"Local Median", None))
        self.local_velocity_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Udiff, Vdiff", None))
        self.local_kernel_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"kernel size", None))
        self.s2n_CB.setText(QCoreApplication.translate("MainWindow", u"Signal 2 Noise", None))
        self.global_std_CB.setText(QCoreApplication.translate("MainWindow", u"Global Std. Deviation", None))
#if QT_CONFIG(whatsthis)
        self.s2n_LE.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.s2n_LE.setText("")
        self.s2n_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"signal/noise", None))
        self.global_std_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"std multiplier", None))
        self.apply_settings_PB.setText(QCoreApplication.translate("MainWindow", u"Apply Settings", None))
        self.load_settings_PB.setText(QCoreApplication.translate("MainWindow", u"Load Settings", None))
        self.save_settings_PB.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        ___qtreewidgetitem = self.files_TW.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Num. Bad Vector", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"File", None));
        self.plot_settings_LE.setText(QCoreApplication.translate("MainWindow", u"b,r,50,2", None))
        self.plot_settings_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"b,r,50,2", None))
        self.BV_settings_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"Show Original BV", None))
        self.BV_settings_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"Show Replaced BV", None))
        self.BV_settings_CB.setItemText(2, QCoreApplication.translate("MainWindow", u"Do Not Show BV", None))
        self.BV_settings_CB.setItemText(3, QCoreApplication.translate("MainWindow", u"Only Show BV", None))

        self.Main_tabs.setTabText(self.Main_tabs.indexOf(self.Validation), QCoreApplication.translate("MainWindow", u"Validation", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Run Progress", None))
        self.run_start_PB.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.run_stop_PB.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Overal Progress", None))
        self.run_progress_TE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Details of the run are shown here...", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Run Settings", None))
        self.process_loadsettings_PB.setText(QCoreApplication.translate("MainWindow", u"Load Settings", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.exp_directory_TB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.exp_experiments_LE.setText("")
        self.exp_experiments_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"experiments naming pattern", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Runs", None))
        self.exp_runs_LE.setText("")
        self.exp_runs_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"runs naming pattern", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Experiments", None))
        self.exp_directory_LE.setText("")
        self.exp_directory_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the experiment directory", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Pattern A", None))
        self.exp_patA_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pattern for frame_a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Pattern B", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Num. of files", None))
        self.exp_patB_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pattern for frame_b", None))
        self.exp_nfiles_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Number of files in each run", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.ExpPage), QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.pre_background_CB.setText(QCoreApplication.translate("MainWindow", u"Remove Background", None))
        self.pre_staticmask_CB.setText(QCoreApplication.translate("MainWindow", u"Static Mask (still under development)", None))
        self.pre_sm_path_TB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pre_dynamicmask_CB.setText(QCoreApplication.translate("MainWindow", u"Dynamic Mask (still under development)", None))
        self.pre_sm_path_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Path to the mask image", None))
        self.pre_bg_nfiles_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Number of files to consider", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.PrePage), QCoreApplication.translate("MainWindow", u"Pre-Process", None))
        self.pro_scale_LE.setText("")
        self.pro_scale_LE.setPlaceholderText("")
        self.pro_searcharea_LE.setText("")
        self.pro_searcharea_LE.setPlaceholderText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Numb. CPU Cores", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Time Step", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Signal/Noise Method", None))
        self.pro_sig2noise_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"peak2peak", None))
        self.pro_sig2noise_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"peak2mean", None))
        self.pro_sig2noise_CB.setItemText(2, QCoreApplication.translate("MainWindow", u"None", None))

        self.pro_timestep_LE.setText("")
        self.pro_timestep_LE.setPlaceholderText("")
        self.pro_ncpus_LE.setText("")
        self.pro_ncpus_LE.setPlaceholderText("")
        self.pro_overlap_LE.setText("")
        self.pro_overlap_LE.setPlaceholderText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Search Area Size", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Window Size", None))
        self.pro_windowsize_LE.setText("")
        self.pro_windowsize_LE.setPlaceholderText("")
        self.toolBox.setItemText(self.toolBox.indexOf(self.ProPage), QCoreApplication.translate("MainWindow", u"Process", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Validation", None))
        self.pos_std_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"std multiplier", None))
#if QT_CONFIG(whatsthis)
        self.pos_s2n_ratio_LE.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pos_s2n_ratio_LE.setText("")
        self.pos_s2n_ratio_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"signal/noise", None))
        self.pos_gv_ulim_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Umin, Umax", None))
        self.pos_std_CB.setText(QCoreApplication.translate("MainWindow", u"Global Std. Deviation", None))
        self.pos_localvelocity_CB.setText(QCoreApplication.translate("MainWindow", u"Local Median", None))
        self.pos_lv_uvdiff_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Udiff, Vdiff", None))
        self.pos_sig2noise_CB.setText(QCoreApplication.translate("MainWindow", u"Signal 2 Noise", None))
        self.pos_globalvelocity_CB.setText(QCoreApplication.translate("MainWindow", u"Global Velocity", None))
        self.pos_lv_kernel_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"kernel size", None))
        self.pos_gv_vlim_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Vmin, Vmax", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Vector Corrections", None))
        self.pos_badvector_CB.setText(QCoreApplication.translate("MainWindow", u"Bad Vectors Replacement", None))
        self.pos_bv_niterations_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Num. of max iterations", None))
        self.pos_bv_method_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"localmean", None))
        self.pos_bv_method_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"disk", None))
        self.pos_bv_method_CB.setItemText(2, QCoreApplication.translate("MainWindow", u"distance", None))

        self.pos_bv_kernel_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Kernel size", None))
        self.pos_smth_factor_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"smoothing coeff. u, v", None))
        self.pos_smoothing_CB.setText(QCoreApplication.translate("MainWindow", u"Vector Smoothing", None))
        self.pos_fm_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ex. rotCW, flipUD", None))
        self.pos_fieldmanip_CB.setText(QCoreApplication.translate("MainWindow", u"Field Manipulations", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Output Mode", None))
        self.pos_output_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"simple", None))
        self.pos_output_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"extended", None))

        self.toolBox.setItemText(self.toolBox.indexOf(self.PosPage), QCoreApplication.translate("MainWindow", u"Post-Process", None))
        self.process_savesettings_PB.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        self.Main_tabs.setTabText(self.Main_tabs.indexOf(self.Process), QCoreApplication.translate("MainWindow", u"Process", None))
        self.freq_exp_GB.setTitle(QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Experiments", None))
        self.freq_exp_LE.setText("")
        self.freq_exp_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"experiments naming pattern", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Runs", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Pattern", None))
        self.freq_pat_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"files naming pattern", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Num. of Files", None))
        self.freq_dir_LE.setText("")
        self.freq_dir_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"path to the experiment directory", None))
        self.freq_dir_TB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.freq_nf_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"number of files to use", None))
        self.freq_run_LE.setText("")
        self.freq_run_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"runs naming pattern", None))
        self.freq_load_from_PB.setText(QCoreApplication.translate("MainWindow", u"Load Experiment Settings From The Process Tab", None))
        self.freq_analysis_GB.setTitle(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Acquisition Frequency", None))
        self.freq_fs_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"fs", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Dimension Factor", None))
        self.freq_dim_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"St=f*(dim_factor)", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Frequency Limit", None))
        self.freq_flim_LE.setText("")
        self.freq_flim_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"highest frequency", None))
        self.freq_pt_fft_CB.setText(QCoreApplication.translate("MainWindow", u"Perform Point FFT", None))
        self.freq_pt_stft_CB.setText(QCoreApplication.translate("MainWindow", u"Perform Point STFT", None))
        self.freq_gb_fft_CB.setText(QCoreApplication.translate("MainWindow", u"Perform Global FFT", None))
        self.freq_gb_stft_CB.setText(QCoreApplication.translate("MainWindow", u"Perform Global STFT", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"STFT", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Data per Segment", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.freq_noverlap_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"overlap", None))
        self.freq_nperseg_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"num. per segment", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Point Location", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Mode            ", None))
        self.freq_pt_loc_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"Max Global Su", None))
        self.freq_pt_loc_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"Max Global Sv", None))
        self.freq_pt_loc_CB.setItemText(2, QCoreApplication.translate("MainWindow", u"Specified Point", None))

        self.freq_pt_loc_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"x, y", None))
        self.freq_load_PB.setText(QCoreApplication.translate("MainWindow", u"Load Settings", None))
        self.freq_save_PB.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        self.freq_run_GB.setTitle(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Run Progress", None))
        self.freq_start_PB.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.freq_stop_PB.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.freq_progress_TE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Details of the run are shown here...", None))
        self.Main_tabs.setTabText(self.Main_tabs.indexOf(self.FrequencyAnalysis), QCoreApplication.translate("MainWindow", u"Freq. Analysis", None))
        self.modal_ana_GB.setTitle(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Num. of Modes ", None))
        self.mdl_rec_CB.setText(QCoreApplication.translate("MainWindow", u"Field Reconstruction", None))
        self.mdl_rec_nm_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Number of modes to use for reconstruction", None))
        self.mdl_nm_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Number of modes to save", None))
        self.mdl_rec_ns_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Number of snapshot to reconstruct", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Num. of Snapshots", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Num. of Modes", None))
        self.mdl_st_CB.setText(QCoreApplication.translate("MainWindow", u"Modal Analysis", None))
        self.mdl_spod_st_CB.setText(QCoreApplication.translate("MainWindow", u"Run SPOD", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Data per Segment", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Overlap", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Windowing", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Acquisition Freq.", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Dimension Factor", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Frequency Limit", None))
        self.mdl_ffield_st_CB.setText(QCoreApplication.translate("MainWindow", u"Extract Frequency Fields", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Method    ", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Frequencies", None))
        self.mdl_ffield_fd_LE.setText("")
        self.mdl_ffield_mt_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"STFT", None))
        self.mdl_ffield_mt_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"FFT", None))

        self.mdl_method_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"Singular Value Decomposition", None))
        self.mdl_method_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"Snapshots Method", None))
        self.mdl_method_CB.setItemText(2, QCoreApplication.translate("MainWindow", u"Spectral POD", None))

        self.mdl_save_PB.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        self.mdl_load_PB.setText(QCoreApplication.translate("MainWindow", u"Load Settings", None))
        self.modal_run_GB.setTitle(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Run Progress", None))
        self.mdl_start_PB.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.mdl_stop_PB.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.mdl_progress_TE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Details of the run are shown here...", None))
        self.modal_exp_GB.setTitle(QCoreApplication.translate("MainWindow", u"Experiment", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Directory", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Experiments", None))
        self.mdl_exp_LE.setText("")
        self.mdl_exp_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"experiments naming pattern", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Runs", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Pattern", None))
        self.mdl_pat_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"files naming pattern", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Num. of Files", None))
        self.mdl_dir_LE.setText("")
        self.mdl_dir_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"path to the experiment directory", None))
        self.mdl_dir_TB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.mdl_nf_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Number of files to use", None))
        self.mdl_run_LE.setText("")
        self.mdl_run_LE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"runs naming pattern", None))
        self.mdl_load_from_PB.setText(QCoreApplication.translate("MainWindow", u"Load Experiment Settings From The Process Tab", None))
        self.Main_tabs.setTabText(self.Main_tabs.indexOf(self.ModalAnalysis), QCoreApplication.translate("MainWindow", u"Modal Analysis", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        pass
    # retranslateUi

