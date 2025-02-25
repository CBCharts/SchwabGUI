# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Lite.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)
import gui.resources.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1169, 1096)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.subCentral = QFrame(self.centralwidget)
        self.subCentral.setObjectName(u"subCentral")
        self.subCentral.setFrameShape(QFrame.Shape.StyledPanel)
        self.subCentral.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.subCentral)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_30 = QFrame(self.subCentral)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.collapse_leftframe_button = QPushButton(self.frame_30)
        self.collapse_leftframe_button.setObjectName(u"collapse_leftframe_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collapse_leftframe_button.sizePolicy().hasHeightForWidth())
        self.collapse_leftframe_button.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/svg/SVG/bars-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.collapse_leftframe_button.setIcon(icon)

        self.horizontalLayout_17.addWidget(self.collapse_leftframe_button)

        self.pushButton_32 = QPushButton(self.frame_30)
        self.pushButton_32.setObjectName(u"pushButton_32")

        self.horizontalLayout_17.addWidget(self.pushButton_32)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_3)

        self.label_10 = QLabel(self.frame_30)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_17.addWidget(self.label_10)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_2)

        self.minimizebutton = QPushButton(self.frame_30)
        self.minimizebutton.setObjectName(u"minimizebutton")
        icon1 = QIcon()
        icon1.addFile(u":/svg/SVG/window-minimize-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizebutton.setIcon(icon1)

        self.horizontalLayout_17.addWidget(self.minimizebutton)

        self.maxbutton = QPushButton(self.frame_30)
        self.maxbutton.setObjectName(u"maxbutton")
        icon2 = QIcon()
        icon2.addFile(u":/svg/SVG/expand-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maxbutton.setIcon(icon2)

        self.horizontalLayout_17.addWidget(self.maxbutton)

        self.closebutton = QPushButton(self.frame_30)
        self.closebutton.setObjectName(u"closebutton")
        icon3 = QIcon()
        icon3.addFile(u":/svg/SVG/circle-xmark-regular.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closebutton.setIcon(icon3)

        self.horizontalLayout_17.addWidget(self.closebutton)


        self.verticalLayout_6.addWidget(self.frame_30)

        self.MidMainCentral = QFrame(self.subCentral)
        self.MidMainCentral.setObjectName(u"MidMainCentral")
        self.MidMainCentral.setFrameShape(QFrame.Shape.NoFrame)
        self.MidMainCentral.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.MidMainCentral)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.LeftMain = QFrame(self.MidMainCentral)
        self.LeftMain.setObjectName(u"LeftMain")
        sizePolicy.setHeightForWidth(self.LeftMain.sizePolicy().hasHeightForWidth())
        self.LeftMain.setSizePolicy(sizePolicy)
        self.LeftMain.setFrameShape(QFrame.Shape.NoFrame)
        self.LeftMain.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.LeftMain)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.CC_button = QPushButton(self.LeftMain)
        self.CC_button.setObjectName(u"CC_button")
        sizePolicy.setHeightForWidth(self.CC_button.sizePolicy().hasHeightForWidth())
        self.CC_button.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Stencil"])
        self.CC_button.setFont(font)
        icon4 = QIcon()
        icon4.addFile(u":/svg/SVG/gear-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.CC_button.setIcon(icon4)
        self.CC_button.setAutoDefault(False)

        self.verticalLayout.addWidget(self.CC_button)

        self.SV_button = QPushButton(self.LeftMain)
        self.SV_button.setObjectName(u"SV_button")
        sizePolicy.setHeightForWidth(self.SV_button.sizePolicy().hasHeightForWidth())
        self.SV_button.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setBold(True)
        self.SV_button.setFont(font1)
        icon5 = QIcon()
        icon5.addFile(u":/svg/SVG/tv-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SV_button.setIcon(icon5)

        self.verticalLayout.addWidget(self.SV_button)

        self.TV_button = QPushButton(self.LeftMain)
        self.TV_button.setObjectName(u"TV_button")
        sizePolicy.setHeightForWidth(self.TV_button.sizePolicy().hasHeightForWidth())
        self.TV_button.setSizePolicy(sizePolicy)
        self.TV_button.setFont(font1)
        icon6 = QIcon()
        icon6.addFile(u":/svg/SVG/shapes-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.TV_button.setIcon(icon6)

        self.verticalLayout.addWidget(self.TV_button)

        self.OW_button = QPushButton(self.LeftMain)
        self.OW_button.setObjectName(u"OW_button")
        sizePolicy.setHeightForWidth(self.OW_button.sizePolicy().hasHeightForWidth())
        self.OW_button.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"OCR A Extended"])
        font2.setPointSize(11)
        font2.setBold(True)
        self.OW_button.setFont(font2)
        icon7 = QIcon()
        icon7.addFile(u":/svg/SVG/solar-panel-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.OW_button.setIcon(icon7)

        self.verticalLayout.addWidget(self.OW_button)

        self.pushButton = QPushButton(self.LeftMain)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font1)
        icon8 = QIcon()
        icon8.addFile(u":/svg/SVG/hashtag-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon8)

        self.verticalLayout.addWidget(self.pushButton)

        self.DOC_button = QPushButton(self.LeftMain)
        self.DOC_button.setObjectName(u"DOC_button")
        sizePolicy.setHeightForWidth(self.DOC_button.sizePolicy().hasHeightForWidth())
        self.DOC_button.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setFamilies([u"Cambria"])
        font3.setPointSize(10)
        font3.setBold(True)
        self.DOC_button.setFont(font3)
        icon9 = QIcon()
        icon9.addFile(u":/svg/SVG/book-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.DOC_button.setIcon(icon9)

        self.verticalLayout.addWidget(self.DOC_button)

        self.frame_60 = QFrame(self.LeftMain)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_60.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.frame_60)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.toolButton_5 = QToolButton(self.frame_60)
        self.toolButton_5.setObjectName(u"toolButton_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolButton_5.sizePolicy().hasHeightForWidth())
        self.toolButton_5.setSizePolicy(sizePolicy1)
        self.toolButton_5.setFont(font1)
        self.toolButton_5.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.toolButton_5.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_5.setArrowType(Qt.ArrowType.NoArrow)

        self.horizontalLayout_33.addWidget(self.toolButton_5)


        self.verticalLayout.addWidget(self.frame_60)

        self.indicator_drop_tableWidget = QTableWidget(self.LeftMain)
        self.indicator_drop_tableWidget.setObjectName(u"indicator_drop_tableWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.indicator_drop_tableWidget.sizePolicy().hasHeightForWidth())
        self.indicator_drop_tableWidget.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.indicator_drop_tableWidget)

        self.frame_59 = QFrame(self.LeftMain)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_59.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_59)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.checkBox_3 = QCheckBox(self.frame_59)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout_20.addWidget(self.checkBox_3, 2, 0, 1, 1)

        self.pushButton_44 = QPushButton(self.frame_59)
        self.pushButton_44.setObjectName(u"pushButton_44")

        self.gridLayout_20.addWidget(self.pushButton_44, 1, 0, 1, 1)

        self.pushButton_45 = QPushButton(self.frame_59)
        self.pushButton_45.setObjectName(u"pushButton_45")

        self.gridLayout_20.addWidget(self.pushButton_45, 2, 1, 1, 1)

        self.pushButton_46 = QPushButton(self.frame_59)
        self.pushButton_46.setObjectName(u"pushButton_46")

        self.gridLayout_20.addWidget(self.pushButton_46, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_59)

        self.label_43 = QLabel(self.LeftMain)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setFont(font1)

        self.verticalLayout.addWidget(self.label_43)

        self.textEdit_4 = QTextEdit(self.LeftMain)
        self.textEdit_4.setObjectName(u"textEdit_4")
        sizePolicy2.setHeightForWidth(self.textEdit_4.sizePolicy().hasHeightForWidth())
        self.textEdit_4.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.textEdit_4)

        self.frame_10 = QFrame(self.LeftMain)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.clear_notes_button = QPushButton(self.frame_10)
        self.clear_notes_button.setObjectName(u"clear_notes_button")

        self.horizontalLayout_16.addWidget(self.clear_notes_button)


        self.verticalLayout.addWidget(self.frame_10)

        self.frame_28 = QFrame(self.LeftMain)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_28)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.np_edit_button = QPushButton(self.frame_28)
        self.np_edit_button.setObjectName(u"np_edit_button")
        icon10 = QIcon()
        icon10.addFile(u":/svg/SVG/pen-to-square-regular.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.np_edit_button.setIcon(icon10)

        self.gridLayout_5.addWidget(self.np_edit_button, 0, 2, 1, 1)

        self.np_new_button = QPushButton(self.frame_28)
        self.np_new_button.setObjectName(u"np_new_button")

        self.gridLayout_5.addWidget(self.np_new_button, 0, 1, 1, 1)

        self.np_next_button = QPushButton(self.frame_28)
        self.np_next_button.setObjectName(u"np_next_button")
        icon11 = QIcon()
        icon11.addFile(u":/svg/SVG/circle-right-regular.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.np_next_button.setIcon(icon11)

        self.gridLayout_5.addWidget(self.np_next_button, 1, 2, 1, 1)

        self.np_prev_button = QPushButton(self.frame_28)
        self.np_prev_button.setObjectName(u"np_prev_button")
        icon12 = QIcon()
        icon12.addFile(u":/svg/SVG/circle-left-regular.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.np_prev_button.setIcon(icon12)

        self.gridLayout_5.addWidget(self.np_prev_button, 1, 0, 1, 1)

        self.np_save_button = QPushButton(self.frame_28)
        self.np_save_button.setObjectName(u"np_save_button")
        icon13 = QIcon()
        icon13.addFile(u":/svg/SVG/floppy-disk-regular.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.np_save_button.setIcon(icon13)

        self.gridLayout_5.addWidget(self.np_save_button, 0, 0, 1, 1)

        self.np_toolbutton = QToolButton(self.frame_28)
        self.np_toolbutton.setObjectName(u"np_toolbutton")
        icon14 = QIcon()
        icon14.addFile(u":/svg/SVG/file-regular.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.np_toolbutton.setIcon(icon14)
        self.np_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.np_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.np_toolbutton.setArrowType(Qt.ArrowType.NoArrow)

        self.gridLayout_5.addWidget(self.np_toolbutton, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_28)


        self.horizontalLayout_6.addWidget(self.LeftMain)

        self.scrollArea_6 = QScrollArea(self.MidMainCentral)
        self.scrollArea_6.setObjectName(u"scrollArea_6")
        self.scrollArea_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 831, 929))
        self.verticalLayout_35 = QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.RightMain = QFrame(self.scrollAreaWidgetContents_6)
        self.RightMain.setObjectName(u"RightMain")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.RightMain.sizePolicy().hasHeightForWidth())
        self.RightMain.setSizePolicy(sizePolicy3)
        self.RightMain.setFrameShape(QFrame.Shape.NoFrame)
        self.RightMain.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.RightMain)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget = QStackedWidget(self.RightMain)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy3.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy3)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea_4 = QScrollArea(self.page_2)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_4.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_4.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 765, 863))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_7 = QFrame(self.scrollAreaWidgetContents_4)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_7)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.frame_13 = QFrame(self.frame_7)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy)
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.p2_startWrap_button = QPushButton(self.frame_13)
        self.p2_startWrap_button.setObjectName(u"p2_startWrap_button")
        sizePolicy.setHeightForWidth(self.p2_startWrap_button.sizePolicy().hasHeightForWidth())
        self.p2_startWrap_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_15.addWidget(self.p2_startWrap_button)

        self.p2_endWrap_button = QPushButton(self.frame_13)
        self.p2_endWrap_button.setObjectName(u"p2_endWrap_button")
        sizePolicy.setHeightForWidth(self.p2_endWrap_button.sizePolicy().hasHeightForWidth())
        self.p2_endWrap_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_15.addWidget(self.p2_endWrap_button)


        self.gridLayout_10.addWidget(self.frame_13, 14, 1, 1, 1)

        self.frame_16 = QFrame(self.frame_7)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_16)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_16)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_AppKey = QLineEdit(self.frame_16)
        self.lineEdit_AppKey.setObjectName(u"lineEdit_AppKey")

        self.gridLayout_2.addWidget(self.lineEdit_AppKey, 1, 2, 1, 1)

        self.lineEdit_RedirectUrl = QLineEdit(self.frame_16)
        self.lineEdit_RedirectUrl.setObjectName(u"lineEdit_RedirectUrl")

        self.gridLayout_2.addWidget(self.lineEdit_RedirectUrl, 4, 2, 1, 1)

        self.label_14 = QLabel(self.frame_16)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 1, 0, 1, 1)

        self.lineEdit_SecretKey = QLineEdit(self.frame_16)
        self.lineEdit_SecretKey.setObjectName(u"lineEdit_SecretKey")

        self.gridLayout_2.addWidget(self.lineEdit_SecretKey, 2, 2, 1, 1)

        self.label_12 = QLabel(self.frame_16)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)

        self.lineEdit_Uri = QLineEdit(self.frame_16)
        self.lineEdit_Uri.setObjectName(u"lineEdit_Uri")

        self.gridLayout_2.addWidget(self.lineEdit_Uri, 3, 2, 1, 1)

        self.label_11 = QLabel(self.frame_16)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)

        self.label_13 = QLabel(self.frame_16)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 2, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_16, 2, 0, 2, 2)

        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")
        font4 = QFont()
        font4.setPointSize(15)
        font4.setBold(True)
        self.label_2.setFont(font4)

        self.gridLayout_10.addWidget(self.label_2, 6, 0, 1, 1)

        self.p2_exp_lineedit = QLineEdit(self.frame_7)
        self.p2_exp_lineedit.setObjectName(u"p2_exp_lineedit")
        self.p2_exp_lineedit.setReadOnly(True)

        self.gridLayout_10.addWidget(self.p2_exp_lineedit, 9, 1, 1, 1)

        self.p2_iv_toolbutton = QToolButton(self.frame_7)
        self.p2_iv_toolbutton.setObjectName(u"p2_iv_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_iv_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_iv_toolbutton.setSizePolicy(sizePolicy)
        self.p2_iv_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_iv_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.p2_iv_toolbutton.setAutoRaise(False)
        self.p2_iv_toolbutton.setArrowType(Qt.ArrowType.NoArrow)

        self.gridLayout_10.addWidget(self.p2_iv_toolbutton, 10, 0, 1, 1)

        self.frame_38 = QFrame(self.frame_7)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_38.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_38)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.p2_vt_toolbutton = QToolButton(self.frame_38)
        self.p2_vt_toolbutton.setObjectName(u"p2_vt_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_vt_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_vt_toolbutton.setSizePolicy(sizePolicy)
        self.p2_vt_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_vt_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_7.addWidget(self.p2_vt_toolbutton, 0, 0, 1, 1)

        self.p2_ec_toolbutton = QToolButton(self.frame_38)
        self.p2_ec_toolbutton.setObjectName(u"p2_ec_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_ec_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_ec_toolbutton.setSizePolicy(sizePolicy)
        self.p2_ec_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_ec_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_7.addWidget(self.p2_ec_toolbutton, 3, 0, 1, 1)

        self.p2_pop_toolbutton = QToolButton(self.frame_38)
        self.p2_pop_toolbutton.setObjectName(u"p2_pop_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_pop_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_pop_toolbutton.setSizePolicy(sizePolicy)
        self.p2_pop_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_pop_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_7.addWidget(self.p2_pop_toolbutton, 0, 1, 1, 1)

        self.p2_eg_toolbutton = QToolButton(self.frame_38)
        self.p2_eg_toolbutton.setObjectName(u"p2_eg_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_eg_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_eg_toolbutton.setSizePolicy(sizePolicy)
        self.p2_eg_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_eg_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_7.addWidget(self.p2_eg_toolbutton, 1, 0, 1, 1)

        self.p2_ev_toolbutton = QToolButton(self.frame_38)
        self.p2_ev_toolbutton.setObjectName(u"p2_ev_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_ev_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_ev_toolbutton.setSizePolicy(sizePolicy)
        self.p2_ev_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_ev_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_7.addWidget(self.p2_ev_toolbutton, 1, 1, 1, 1)

        self.p2_ed_toolbutton = QToolButton(self.frame_38)
        self.p2_ed_toolbutton.setObjectName(u"p2_ed_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_ed_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_ed_toolbutton.setSizePolicy(sizePolicy)
        self.p2_ed_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_ed_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_7.addWidget(self.p2_ed_toolbutton, 3, 1, 1, 1)


        self.gridLayout_10.addWidget(self.frame_38, 13, 1, 1, 1)

        self.frame_41 = QFrame(self.frame_7)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_41.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.p2_auth_button = QPushButton(self.frame_41)
        self.p2_auth_button.setObjectName(u"p2_auth_button")

        self.horizontalLayout_23.addWidget(self.p2_auth_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer)

        self.p2_getToken_button = QPushButton(self.frame_41)
        self.p2_getToken_button.setObjectName(u"p2_getToken_button")

        self.horizontalLayout_23.addWidget(self.p2_getToken_button)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_4)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_15)


        self.gridLayout_10.addWidget(self.frame_41, 5, 0, 1, 2)

        self.frame_39 = QFrame(self.frame_7)
        self.frame_39.setObjectName(u"frame_39")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_39.sizePolicy().hasHeightForWidth())
        self.frame_39.setSizePolicy(sizePolicy4)
        font5 = QFont()
        font5.setBold(False)
        self.frame_39.setFont(font5)
        self.frame_39.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_39.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_13)

        self.label_18 = QLabel(self.frame_39)
        self.label_18.setObjectName(u"label_18")
        sizePolicy4.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy4)
        font6 = QFont()
        font6.setPointSize(8)
        font6.setBold(True)
        font6.setKerning(False)
        self.label_18.setFont(font6)
        self.label_18.setScaledContents(True)
        self.label_18.setWordWrap(False)

        self.horizontalLayout_21.addWidget(self.label_18)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_14)


        self.gridLayout_10.addWidget(self.frame_39, 12, 1, 1, 1)

        self.p2_exp_toolbutton = QToolButton(self.frame_7)
        self.p2_exp_toolbutton.setObjectName(u"p2_exp_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_exp_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_exp_toolbutton.setSizePolicy(sizePolicy)
        self.p2_exp_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_exp_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_10.addWidget(self.p2_exp_toolbutton, 9, 0, 1, 1)

        self.p2_interval_lineedit = QLineEdit(self.frame_7)
        self.p2_interval_lineedit.setObjectName(u"p2_interval_lineedit")
        self.p2_interval_lineedit.setReadOnly(True)

        self.gridLayout_10.addWidget(self.p2_interval_lineedit, 7, 1, 1, 1)

        self.p2_index_lineedit = QLineEdit(self.frame_7)
        self.p2_index_lineedit.setObjectName(u"p2_index_lineedit")
        self.p2_index_lineedit.setReadOnly(True)

        self.gridLayout_10.addWidget(self.p2_index_lineedit, 8, 1, 1, 1)

        self.p2_iv_lineedit = QLineEdit(self.frame_7)
        self.p2_iv_lineedit.setObjectName(u"p2_iv_lineedit")
        self.p2_iv_lineedit.setReadOnly(True)

        self.gridLayout_10.addWidget(self.p2_iv_lineedit, 10, 1, 1, 1)

        self.p2_interval_toolbutton = QToolButton(self.frame_7)
        self.p2_interval_toolbutton.setObjectName(u"p2_interval_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_interval_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_interval_toolbutton.setSizePolicy(sizePolicy)
        self.p2_interval_toolbutton.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.p2_interval_toolbutton.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.p2_interval_toolbutton.setToolTipDuration(0)
        self.p2_interval_toolbutton.setAutoExclusive(False)
        self.p2_interval_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_interval_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.p2_interval_toolbutton.setAutoRaise(False)

        self.gridLayout_10.addWidget(self.p2_interval_toolbutton, 7, 0, 1, 1)

        self.p2_index_toolbutton = QToolButton(self.frame_7)
        self.p2_index_toolbutton.setObjectName(u"p2_index_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_index_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_index_toolbutton.setSizePolicy(sizePolicy)
        self.p2_index_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_index_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_10.addWidget(self.p2_index_toolbutton, 8, 0, 1, 1)

        self.label_9 = QLabel(self.frame_7)
        self.label_9.setObjectName(u"label_9")
        font7 = QFont()
        font7.setFamilies([u"Stencil"])
        font7.setPointSize(32)
        font7.setBold(True)
        font7.setUnderline(True)
        self.label_9.setFont(font7)

        self.gridLayout_10.addWidget(self.label_9, 1, 1, 1, 1)

        self.p2_kClean_toolbutton = QToolButton(self.frame_7)
        self.p2_kClean_toolbutton.setObjectName(u"p2_kClean_toolbutton")
        sizePolicy.setHeightForWidth(self.p2_kClean_toolbutton.sizePolicy().hasHeightForWidth())
        self.p2_kClean_toolbutton.setSizePolicy(sizePolicy)
        self.p2_kClean_toolbutton.setFont(font5)
        self.p2_kClean_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p2_kClean_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_10.addWidget(self.p2_kClean_toolbutton, 11, 0, 1, 1)

        self.p2_kClean_lineedit = QLineEdit(self.frame_7)
        self.p2_kClean_lineedit.setObjectName(u"p2_kClean_lineedit")

        self.gridLayout_10.addWidget(self.p2_kClean_lineedit, 11, 1, 1, 1)

        self.frame_11 = QFrame(self.frame_7)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.frame_11)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.clearCache_button = QPushButton(self.frame_11)
        self.clearCache_button.setObjectName(u"clearCache_button")
        sizePolicy.setHeightForWidth(self.clearCache_button.sizePolicy().hasHeightForWidth())
        self.clearCache_button.setSizePolicy(sizePolicy)

        self.verticalLayout_40.addWidget(self.clearCache_button)

        self.clearNotes_button = QPushButton(self.frame_11)
        self.clearNotes_button.setObjectName(u"clearNotes_button")
        sizePolicy.setHeightForWidth(self.clearNotes_button.sizePolicy().hasHeightForWidth())
        self.clearNotes_button.setSizePolicy(sizePolicy)

        self.verticalLayout_40.addWidget(self.clearNotes_button)

        self.clearHist_toolbutton = QToolButton(self.frame_11)
        self.clearHist_toolbutton.setObjectName(u"clearHist_toolbutton")
        sizePolicy.setHeightForWidth(self.clearHist_toolbutton.sizePolicy().hasHeightForWidth())
        self.clearHist_toolbutton.setSizePolicy(sizePolicy)
        self.clearHist_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.clearHist_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_40.addWidget(self.clearHist_toolbutton)


        self.gridLayout_10.addWidget(self.frame_11, 14, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.frame_7)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_2.addWidget(self.scrollArea_4)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_16 = QVBoxLayout(self.page_3)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.scrollArea_5 = QScrollArea(self.page_3)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 777, 875))
        self.verticalLayout_34 = QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.frame_9 = QFrame(self.scrollAreaWidgetContents_5)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_9)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_9, 1, 6, 1, 1)

        self.lineEdit_5 = QLineEdit(self.frame_9)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.gridLayout_16.addWidget(self.lineEdit_5, 1, 3, 1, 1)

        self.label_44 = QLabel(self.frame_9)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_16.addWidget(self.label_44, 1, 1, 1, 1)

        self.p3_startRe_button = QPushButton(self.frame_9)
        self.p3_startRe_button.setObjectName(u"p3_startRe_button")
        icon15 = QIcon()
        icon15.addFile(u":/svg/SVG/play-solid (1).svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.p3_startRe_button.setIcon(icon15)

        self.gridLayout_16.addWidget(self.p3_startRe_button, 1, 4, 1, 1)

        self.p3_interval_drop = QToolButton(self.frame_9)
        self.p3_interval_drop.setObjectName(u"p3_interval_drop")
        icon16 = QIcon()
        icon16.addFile(u":/svg/SVG/clock-rotate-left-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.p3_interval_drop.setIcon(icon16)
        self.p3_interval_drop.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p3_interval_drop.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_16.addWidget(self.p3_interval_drop, 1, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_6, 1, 7, 1, 1)

        self.p3_refresh_button = QPushButton(self.frame_9)
        self.p3_refresh_button.setObjectName(u"p3_refresh_button")
        icon17 = QIcon()
        icon17.addFile(u":/svg/SVG/arrow-rotate-right-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.p3_refresh_button.setIcon(icon17)

        self.gridLayout_16.addWidget(self.p3_refresh_button, 1, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_5, 1, 8, 1, 1)

        self.p3_endRe_button = QPushButton(self.frame_9)
        self.p3_endRe_button.setObjectName(u"p3_endRe_button")
        icon18 = QIcon()
        icon18.addFile(u":/svg/SVG/ban-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.p3_endRe_button.setIcon(icon18)

        self.gridLayout_16.addWidget(self.p3_endRe_button, 1, 5, 1, 1)

        self.label_48 = QLabel(self.frame_9)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font1)

        self.gridLayout_16.addWidget(self.label_48, 0, 0, 1, 1)


        self.verticalLayout_34.addWidget(self.frame_9)

        self.frame_33 = QFrame(self.scrollAreaWidgetContents_5)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_33)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.frame_29 = QFrame(self.frame_33)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_29)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.lineEdit_index_p3 = QLineEdit(self.frame_29)
        self.lineEdit_index_p3.setObjectName(u"lineEdit_index_p3")

        self.gridLayout_15.addWidget(self.lineEdit_index_p3, 1, 1, 1, 1)

        self.toolButton_3 = QToolButton(self.frame_29)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.toolButton_3.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_15.addWidget(self.toolButton_3, 1, 2, 1, 1)

        self.lineEdit_3 = QLineEdit(self.frame_29)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout_15.addWidget(self.lineEdit_3, 1, 3, 1, 1)

        self.toolButton_index_p3 = QToolButton(self.frame_29)
        self.toolButton_index_p3.setObjectName(u"toolButton_index_p3")
        self.toolButton_index_p3.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.toolButton_index_p3.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_15.addWidget(self.toolButton_index_p3, 1, 0, 1, 1)

        self.label_47 = QLabel(self.frame_29)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font1)

        self.gridLayout_15.addWidget(self.label_47, 0, 0, 1, 1)


        self.verticalLayout_17.addWidget(self.frame_29)

        self.frame_34 = QFrame(self.frame_33)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_34.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_34)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.lineEdit_4 = QLineEdit(self.frame_34)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout_13.addWidget(self.lineEdit_4, 2, 7, 1, 1)

        self.toolButton_4 = QToolButton(self.frame_34)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.toolButton_4.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_13.addWidget(self.toolButton_4, 2, 6, 1, 1)

        self.lineEdit_2 = QLineEdit(self.frame_34)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_13.addWidget(self.lineEdit_2, 2, 3, 1, 1)

        self.pushButton_3 = QPushButton(self.frame_34)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_13.addWidget(self.pushButton_3, 2, 8, 1, 1)

        self.label_45 = QLabel(self.frame_34)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font1)

        self.gridLayout_13.addWidget(self.label_45, 1, 0, 1, 1)

        self.toolButton_2 = QToolButton(self.frame_34)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.toolButton_2.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.gridLayout_13.addWidget(self.toolButton_2, 2, 0, 1, 1)


        self.verticalLayout_17.addWidget(self.frame_34)

        self.frame_17 = QFrame(self.frame_33)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_17)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.pushButton_4 = QPushButton(self.frame_17)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout_14.addWidget(self.pushButton_4, 1, 3, 1, 1)

        self.label_46 = QLabel(self.frame_17)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font1)

        self.gridLayout_14.addWidget(self.label_46, 0, 0, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_16, 1, 4, 1, 1)

        self.lineEdit_10 = QLineEdit(self.frame_17)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.gridLayout_14.addWidget(self.lineEdit_10, 1, 2, 1, 1)

        self.toolButton_10 = QToolButton(self.frame_17)
        self.toolButton_10.setObjectName(u"toolButton_10")

        self.gridLayout_14.addWidget(self.toolButton_10, 1, 0, 1, 1)


        self.verticalLayout_17.addWidget(self.frame_17)

        self.frame_35 = QFrame(self.frame_33)
        self.frame_35.setObjectName(u"frame_35")
        sizePolicy3.setHeightForWidth(self.frame_35.sizePolicy().hasHeightForWidth())
        self.frame_35.setSizePolicy(sizePolicy3)
        self.frame_35.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_35.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_35)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.p3_wev = QWebEngineView(self.frame_35)
        self.p3_wev.setObjectName(u"p3_wev")
        self.p3_wev.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_18.addWidget(self.p3_wev)


        self.verticalLayout_17.addWidget(self.frame_35)


        self.verticalLayout_34.addWidget(self.frame_33)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)

        self.verticalLayout_16.addWidget(self.scrollArea_5)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_9 = QVBoxLayout(self.page_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.scrollArea_3 = QScrollArea(self.page_4)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_3.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 1536, 1936))
        self.verticalLayout_33 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.frame_3 = QFrame(self.scrollAreaWidgetContents_3)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy3.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy3)
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_27 = QFrame(self.frame_3)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.checkBox_2 = QCheckBox(self.frame_27)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_13.addWidget(self.checkBox_2)

        self.p4_interval_button = QToolButton(self.frame_27)
        self.p4_interval_button.setObjectName(u"p4_interval_button")
        sizePolicy.setHeightForWidth(self.p4_interval_button.sizePolicy().hasHeightForWidth())
        self.p4_interval_button.setSizePolicy(sizePolicy)
        self.p4_interval_button.setIcon(icon16)
        self.p4_interval_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout_13.addWidget(self.p4_interval_button)

        self.p4_start_button = QPushButton(self.frame_27)
        self.p4_start_button.setObjectName(u"p4_start_button")
        self.p4_start_button.setIcon(icon15)

        self.horizontalLayout_13.addWidget(self.p4_start_button)

        self.p4_end_button = QPushButton(self.frame_27)
        self.p4_end_button.setObjectName(u"p4_end_button")
        self.p4_end_button.setIcon(icon18)

        self.horizontalLayout_13.addWidget(self.p4_end_button)

        self.p4_refresh_button = QPushButton(self.frame_27)
        self.p4_refresh_button.setObjectName(u"p4_refresh_button")
        self.p4_refresh_button.setIcon(icon17)

        self.horizontalLayout_13.addWidget(self.p4_refresh_button)

        self.p4_hideL_button = QPushButton(self.frame_27)
        self.p4_hideL_button.setObjectName(u"p4_hideL_button")

        self.horizontalLayout_13.addWidget(self.p4_hideL_button)

        self.p4_hideR_button = QPushButton(self.frame_27)
        self.p4_hideR_button.setObjectName(u"p4_hideR_button")

        self.horizontalLayout_13.addWidget(self.p4_hideR_button)

        self.pushButton_2 = QPushButton(self.frame_27)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_13.addWidget(self.pushButton_2)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_17)


        self.gridLayout_3.addWidget(self.frame_27, 0, 0, 1, 1)

        self.frame_14 = QFrame(self.frame_3)
        self.frame_14.setObjectName(u"frame_14")
        sizePolicy3.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy3)
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.p4_Lframe = QFrame(self.frame_14)
        self.p4_Lframe.setObjectName(u"p4_Lframe")
        sizePolicy3.setHeightForWidth(self.p4_Lframe.sizePolicy().hasHeightForWidth())
        self.p4_Lframe.setSizePolicy(sizePolicy3)
        self.p4_Lframe.setFrameShape(QFrame.Shape.NoFrame)
        self.p4_Lframe.setFrameShadow(QFrame.Shadow.Raised)
        self.p4_Lframe.setLineWidth(1)
        self.verticalLayout_10 = QVBoxLayout(self.p4_Lframe)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.p4_v1_drop = QToolButton(self.p4_Lframe)
        self.p4_v1_drop.setObjectName(u"p4_v1_drop")
        sizePolicy.setHeightForWidth(self.p4_v1_drop.sizePolicy().hasHeightForWidth())
        self.p4_v1_drop.setSizePolicy(sizePolicy)
        self.p4_v1_drop.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.verticalLayout_10.addWidget(self.p4_v1_drop)

        self.p4_wev1 = QWebEngineView(self.p4_Lframe)
        self.p4_wev1.setObjectName(u"p4_wev1")
        sizePolicy3.setHeightForWidth(self.p4_wev1.sizePolicy().hasHeightForWidth())
        self.p4_wev1.setSizePolicy(sizePolicy3)
        self.p4_wev1.setMinimumSize(QSize(720, 700))
        self.p4_wev1.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_10.addWidget(self.p4_wev1)

        self.p4_v2_drop = QToolButton(self.p4_Lframe)
        self.p4_v2_drop.setObjectName(u"p4_v2_drop")
        sizePolicy1.setHeightForWidth(self.p4_v2_drop.sizePolicy().hasHeightForWidth())
        self.p4_v2_drop.setSizePolicy(sizePolicy1)
        self.p4_v2_drop.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.p4_v2_drop.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.verticalLayout_10.addWidget(self.p4_v2_drop)

        self.p4_wev2 = QWebEngineView(self.p4_Lframe)
        self.p4_wev2.setObjectName(u"p4_wev2")
        sizePolicy3.setHeightForWidth(self.p4_wev2.sizePolicy().hasHeightForWidth())
        self.p4_wev2.setSizePolicy(sizePolicy3)
        self.p4_wev2.setMinimumSize(QSize(720, 700))
        self.p4_wev2.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_10.addWidget(self.p4_wev2)

        self.frame_31 = QFrame(self.p4_Lframe)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_31)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.tableWidget_3 = QTableWidget(self.frame_31)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        sizePolicy.setHeightForWidth(self.tableWidget_3.sizePolicy().hasHeightForWidth())
        self.tableWidget_3.setSizePolicy(sizePolicy)
        self.tableWidget_3.setMinimumSize(QSize(0, 192))

        self.gridLayout_18.addWidget(self.tableWidget_3, 0, 0, 1, 1)

        self.p4_lowframe_2 = QFrame(self.frame_31)
        self.p4_lowframe_2.setObjectName(u"p4_lowframe_2")
        self.p4_lowframe_2.setFrameShape(QFrame.Shape.NoFrame)
        self.p4_lowframe_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.p4_lowframe_2)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.pushButton_14 = QPushButton(self.p4_lowframe_2)
        self.pushButton_14.setObjectName(u"pushButton_14")

        self.gridLayout_17.addWidget(self.pushButton_14, 1, 1, 1, 1)

        self.pushButton_10 = QPushButton(self.p4_lowframe_2)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.gridLayout_17.addWidget(self.pushButton_10, 1, 2, 1, 1)

        self.pushButton_8 = QPushButton(self.p4_lowframe_2)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.gridLayout_17.addWidget(self.pushButton_8, 3, 1, 1, 1)

        self.label_53 = QLabel(self.p4_lowframe_2)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_17.addWidget(self.label_53, 1, 0, 1, 1)

        self.label_54 = QLabel(self.p4_lowframe_2)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_17.addWidget(self.label_54, 3, 0, 1, 1)

        self.pushButton_15 = QPushButton(self.p4_lowframe_2)
        self.pushButton_15.setObjectName(u"pushButton_15")

        self.gridLayout_17.addWidget(self.pushButton_15, 2, 2, 1, 1)

        self.label_55 = QLabel(self.p4_lowframe_2)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_17.addWidget(self.label_55, 2, 0, 1, 1)

        self.label_56 = QLabel(self.p4_lowframe_2)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_17.addWidget(self.label_56, 0, 0, 1, 1)

        self.pushButton_16 = QPushButton(self.p4_lowframe_2)
        self.pushButton_16.setObjectName(u"pushButton_16")

        self.gridLayout_17.addWidget(self.pushButton_16, 0, 2, 1, 1)

        self.pushButton_17 = QPushButton(self.p4_lowframe_2)
        self.pushButton_17.setObjectName(u"pushButton_17")
        sizePolicy1.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy1)

        self.gridLayout_17.addWidget(self.pushButton_17, 0, 1, 1, 1)

        self.pushButton_18 = QPushButton(self.p4_lowframe_2)
        self.pushButton_18.setObjectName(u"pushButton_18")

        self.gridLayout_17.addWidget(self.pushButton_18, 2, 1, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_18, 0, 3, 1, 1)


        self.gridLayout_18.addWidget(self.p4_lowframe_2, 1, 0, 1, 1)


        self.verticalLayout_10.addWidget(self.frame_31)


        self.horizontalLayout_14.addWidget(self.p4_Lframe)

        self.p4_Rframe = QFrame(self.frame_14)
        self.p4_Rframe.setObjectName(u"p4_Rframe")
        sizePolicy3.setHeightForWidth(self.p4_Rframe.sizePolicy().hasHeightForWidth())
        self.p4_Rframe.setSizePolicy(sizePolicy3)
        self.p4_Rframe.setFrameShape(QFrame.Shape.NoFrame)
        self.p4_Rframe.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.p4_Rframe)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.p4_v3_drop = QToolButton(self.p4_Rframe)
        self.p4_v3_drop.setObjectName(u"p4_v3_drop")
        sizePolicy.setHeightForWidth(self.p4_v3_drop.sizePolicy().hasHeightForWidth())
        self.p4_v3_drop.setSizePolicy(sizePolicy)
        self.p4_v3_drop.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.verticalLayout_11.addWidget(self.p4_v3_drop)

        self.p4_wev3 = QWebEngineView(self.p4_Rframe)
        self.p4_wev3.setObjectName(u"p4_wev3")
        sizePolicy3.setHeightForWidth(self.p4_wev3.sizePolicy().hasHeightForWidth())
        self.p4_wev3.setSizePolicy(sizePolicy3)
        self.p4_wev3.setMinimumSize(QSize(720, 700))
        self.p4_wev3.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_11.addWidget(self.p4_wev3)

        self.frame_32 = QFrame(self.p4_Rframe)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_32)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableWidget_2 = QTableWidget(self.frame_32)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        sizePolicy.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.tableWidget_2)

        self.p4_lowframe = QFrame(self.frame_32)
        self.p4_lowframe.setObjectName(u"p4_lowframe")
        self.p4_lowframe.setFrameShape(QFrame.Shape.NoFrame)
        self.p4_lowframe.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.p4_lowframe)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.pushButton_12 = QPushButton(self.p4_lowframe)
        self.pushButton_12.setObjectName(u"pushButton_12")

        self.gridLayout_8.addWidget(self.pushButton_12, 1, 1, 1, 1)

        self.pushButton_9 = QPushButton(self.p4_lowframe)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.gridLayout_8.addWidget(self.pushButton_9, 1, 2, 1, 1)

        self.pushButton_6 = QPushButton(self.p4_lowframe)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.gridLayout_8.addWidget(self.pushButton_6, 3, 1, 1, 1)

        self.label_50 = QLabel(self.p4_lowframe)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_8.addWidget(self.label_50, 1, 0, 1, 1)

        self.label_52 = QLabel(self.p4_lowframe)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_8.addWidget(self.label_52, 3, 0, 1, 1)

        self.pushButton_7 = QPushButton(self.p4_lowframe)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.gridLayout_8.addWidget(self.pushButton_7, 2, 2, 1, 1)

        self.label_51 = QLabel(self.p4_lowframe)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_8.addWidget(self.label_51, 2, 0, 1, 1)

        self.label_49 = QLabel(self.p4_lowframe)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_8.addWidget(self.label_49, 0, 0, 1, 1)

        self.pushButton_13 = QPushButton(self.p4_lowframe)
        self.pushButton_13.setObjectName(u"pushButton_13")

        self.gridLayout_8.addWidget(self.pushButton_13, 0, 2, 1, 1)

        self.pushButton_11 = QPushButton(self.p4_lowframe)
        self.pushButton_11.setObjectName(u"pushButton_11")
        sizePolicy1.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.pushButton_11, 0, 1, 1, 1)

        self.pushButton_5 = QPushButton(self.p4_lowframe)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout_8.addWidget(self.pushButton_5, 2, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_10, 0, 3, 1, 1)


        self.verticalLayout_5.addWidget(self.p4_lowframe)


        self.verticalLayout_11.addWidget(self.frame_32)


        self.horizontalLayout_14.addWidget(self.p4_Rframe)


        self.gridLayout_3.addWidget(self.frame_14, 1, 0, 1, 1)


        self.verticalLayout_33.addWidget(self.frame_3)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_9.addWidget(self.scrollArea_3)

        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_14 = QVBoxLayout(self.page_5)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.frame_25 = QFrame(self.page_5)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.label_15 = QLabel(self.frame_25)
        self.label_15.setObjectName(u"label_15")
        font8 = QFont()
        font8.setFamilies([u"OCR A Extended"])
        font8.setPointSize(15)
        font8.setBold(True)
        font8.setStrikeOut(False)
        self.label_15.setFont(font8)

        self.horizontalLayout_2.addWidget(self.label_15)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_8)


        self.verticalLayout_14.addWidget(self.frame_25)

        self.frame_40 = QFrame(self.page_5)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_40.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_40)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_19, 5, 7, 1, 1)

        self.pushButton_24 = QPushButton(self.frame_40)
        self.pushButton_24.setObjectName(u"pushButton_24")
        self.pushButton_24.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_24, 5, 4, 1, 1)

        self.p5_hideC2 = QPushButton(self.frame_40)
        self.p5_hideC2.setObjectName(u"p5_hideC2")
        self.p5_hideC2.setCheckable(True)

        self.gridLayout_19.addWidget(self.p5_hideC2, 9, 1, 1, 1)

        self.label_57 = QLabel(self.frame_40)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setFont(font1)

        self.gridLayout_19.addWidget(self.label_57, 1, 0, 1, 1)

        self.pushButton_20 = QPushButton(self.frame_40)
        self.pushButton_20.setObjectName(u"pushButton_20")
        self.pushButton_20.setCheckable(True)
        self.pushButton_20.setAutoDefault(False)
        self.pushButton_20.setFlat(False)

        self.gridLayout_19.addWidget(self.pushButton_20, 2, 1, 1, 1)

        self.p5_interval_toolbutton = QToolButton(self.frame_40)
        self.p5_interval_toolbutton.setObjectName(u"p5_interval_toolbutton")
        self.p5_interval_toolbutton.setIcon(icon16)
        self.p5_interval_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.gridLayout_19.addWidget(self.p5_interval_toolbutton, 0, 0, 1, 1)

        self.pushButton_19 = QPushButton(self.frame_40)
        self.pushButton_19.setObjectName(u"pushButton_19")
        self.pushButton_19.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_19, 2, 0, 1, 1)

        self.checkBox = QCheckBox(self.frame_40)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_19.addWidget(self.checkBox, 0, 1, 1, 1)

        self.p5_start_button = QPushButton(self.frame_40)
        self.p5_start_button.setObjectName(u"p5_start_button")
        self.p5_start_button.setIcon(icon15)

        self.gridLayout_19.addWidget(self.p5_start_button, 0, 4, 1, 1)

        self.p5_hideC1 = QPushButton(self.frame_40)
        self.p5_hideC1.setObjectName(u"p5_hideC1")
        self.p5_hideC1.setCheckable(True)

        self.gridLayout_19.addWidget(self.p5_hideC1, 9, 0, 1, 1)

        self.p5_hideC3 = QPushButton(self.frame_40)
        self.p5_hideC3.setObjectName(u"p5_hideC3")
        self.p5_hideC3.setCheckable(True)

        self.gridLayout_19.addWidget(self.p5_hideC3, 9, 2, 1, 1)

        self.p5_manual_button = QPushButton(self.frame_40)
        self.p5_manual_button.setObjectName(u"p5_manual_button")
        self.p5_manual_button.setIcon(icon17)

        self.gridLayout_19.addWidget(self.p5_manual_button, 0, 2, 1, 1)

        self.pushButton_21 = QPushButton(self.frame_40)
        self.pushButton_21.setObjectName(u"pushButton_21")
        self.pushButton_21.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_21, 5, 0, 1, 1)

        self.label_59 = QLabel(self.frame_40)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font1)

        self.gridLayout_19.addWidget(self.label_59, 8, 0, 1, 1)

        self.label_58 = QLabel(self.frame_40)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setFont(font1)

        self.gridLayout_19.addWidget(self.label_58, 3, 0, 1, 1)

        self.pushButton_22 = QPushButton(self.frame_40)
        self.pushButton_22.setObjectName(u"pushButton_22")
        self.pushButton_22.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_22, 5, 1, 1, 1)

        self.label_60 = QLabel(self.frame_40)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font1)

        self.gridLayout_19.addWidget(self.label_60, 6, 0, 1, 1)

        self.p5_end_button = QPushButton(self.frame_40)
        self.p5_end_button.setObjectName(u"p5_end_button")
        self.p5_end_button.setIcon(icon18)

        self.gridLayout_19.addWidget(self.p5_end_button, 0, 6, 1, 1)

        self.pushButton_23 = QPushButton(self.frame_40)
        self.pushButton_23.setObjectName(u"pushButton_23")
        self.pushButton_23.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_23, 5, 2, 1, 1)

        self.pushButton_25 = QPushButton(self.frame_40)
        self.pushButton_25.setObjectName(u"pushButton_25")
        self.pushButton_25.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_25, 7, 0, 1, 1)

        self.pushButton_26 = QPushButton(self.frame_40)
        self.pushButton_26.setObjectName(u"pushButton_26")
        self.pushButton_26.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_26, 7, 1, 1, 1)

        self.pushButton_27 = QPushButton(self.frame_40)
        self.pushButton_27.setObjectName(u"pushButton_27")
        self.pushButton_27.setCheckable(True)

        self.gridLayout_19.addWidget(self.pushButton_27, 7, 2, 1, 1)


        self.verticalLayout_14.addWidget(self.frame_40)

        self.scrollArea_2 = QScrollArea(self.page_5)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1812, 2691))
        self.verticalLayout_27 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.frame_15 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_15.setObjectName(u"frame_15")
        sizePolicy3.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy3)
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.p5_fLeft = QFrame(self.frame_15)
        self.p5_fLeft.setObjectName(u"p5_fLeft")
        sizePolicy3.setHeightForWidth(self.p5_fLeft.sizePolicy().hasHeightForWidth())
        self.p5_fLeft.setSizePolicy(sizePolicy3)
        self.p5_fLeft.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_fLeft.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.p5_fLeft)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.frame_18 = QFrame(self.p5_fLeft)
        self.frame_18.setObjectName(u"frame_18")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_18.sizePolicy().hasHeightForWidth())
        self.frame_18.setSizePolicy(sizePolicy5)
        self.frame_18.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.p5_gex_hide = QPushButton(self.frame_18)
        self.p5_gex_hide.setObjectName(u"p5_gex_hide")

        self.horizontalLayout_5.addWidget(self.p5_gex_hide)

        self.label_GEX_Top = QLabel(self.frame_18)
        self.label_GEX_Top.setObjectName(u"label_GEX_Top")
        sizePolicy5.setHeightForWidth(self.label_GEX_Top.sizePolicy().hasHeightForWidth())
        self.label_GEX_Top.setSizePolicy(sizePolicy5)
        self.label_GEX_Top.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_GEX_Top)

        self.p5_gex_info = QPushButton(self.frame_18)
        self.p5_gex_info.setObjectName(u"p5_gex_info")
        sizePolicy.setHeightForWidth(self.p5_gex_info.sizePolicy().hasHeightForWidth())
        self.p5_gex_info.setSizePolicy(sizePolicy)
        icon19 = QIcon()
        icon19.addFile(u":/svg/SVG/circle-info-solid.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.p5_gex_info.setIcon(icon19)

        self.horizontalLayout_5.addWidget(self.p5_gex_info)


        self.verticalLayout_13.addWidget(self.frame_18)

        self.p5_gex_frame = QFrame(self.p5_fLeft)
        self.p5_gex_frame.setObjectName(u"p5_gex_frame")
        sizePolicy3.setHeightForWidth(self.p5_gex_frame.sizePolicy().hasHeightForWidth())
        self.p5_gex_frame.setSizePolicy(sizePolicy3)
        self.p5_gex_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_gex_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.p5_gex_frame)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.p5_gex_web = QWebEngineView(self.p5_gex_frame)
        self.p5_gex_web.setObjectName(u"p5_gex_web")
        sizePolicy3.setHeightForWidth(self.p5_gex_web.sizePolicy().hasHeightForWidth())
        self.p5_gex_web.setSizePolicy(sizePolicy3)
        self.p5_gex_web.setMinimumSize(QSize(700, 680))
        self.p5_gex_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_19.addWidget(self.p5_gex_web)


        self.verticalLayout_13.addWidget(self.p5_gex_frame)

        self.frame_19 = QFrame(self.p5_fLeft)
        self.frame_19.setObjectName(u"frame_19")
        sizePolicy5.setHeightForWidth(self.frame_19.sizePolicy().hasHeightForWidth())
        self.frame_19.setSizePolicy(sizePolicy5)
        self.frame_19.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.p5_dex_hide = QPushButton(self.frame_19)
        self.p5_dex_hide.setObjectName(u"p5_dex_hide")

        self.horizontalLayout_11.addWidget(self.p5_dex_hide)

        self.label_DEX_Top = QLabel(self.frame_19)
        self.label_DEX_Top.setObjectName(u"label_DEX_Top")
        sizePolicy5.setHeightForWidth(self.label_DEX_Top.sizePolicy().hasHeightForWidth())
        self.label_DEX_Top.setSizePolicy(sizePolicy5)
        self.label_DEX_Top.setFont(font1)

        self.horizontalLayout_11.addWidget(self.label_DEX_Top)

        self.p5_dex_info = QPushButton(self.frame_19)
        self.p5_dex_info.setObjectName(u"p5_dex_info")
        sizePolicy.setHeightForWidth(self.p5_dex_info.sizePolicy().hasHeightForWidth())
        self.p5_dex_info.setSizePolicy(sizePolicy)
        self.p5_dex_info.setIcon(icon19)

        self.horizontalLayout_11.addWidget(self.p5_dex_info)


        self.verticalLayout_13.addWidget(self.frame_19)

        self.p5_dex_frame = QFrame(self.p5_fLeft)
        self.p5_dex_frame.setObjectName(u"p5_dex_frame")
        sizePolicy3.setHeightForWidth(self.p5_dex_frame.sizePolicy().hasHeightForWidth())
        self.p5_dex_frame.setSizePolicy(sizePolicy3)
        self.p5_dex_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_dex_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.p5_dex_frame)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.p5_dex_web = QWebEngineView(self.p5_dex_frame)
        self.p5_dex_web.setObjectName(u"p5_dex_web")
        sizePolicy3.setHeightForWidth(self.p5_dex_web.sizePolicy().hasHeightForWidth())
        self.p5_dex_web.setSizePolicy(sizePolicy3)
        self.p5_dex_web.setMinimumSize(QSize(700, 680))
        self.p5_dex_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_20.addWidget(self.p5_dex_web)


        self.verticalLayout_13.addWidget(self.p5_dex_frame)

        self.frame_20 = QFrame(self.p5_fLeft)
        self.frame_20.setObjectName(u"frame_20")
        sizePolicy5.setHeightForWidth(self.frame_20.sizePolicy().hasHeightForWidth())
        self.frame_20.setSizePolicy(sizePolicy5)
        self.frame_20.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.p5_cex_hide = QPushButton(self.frame_20)
        self.p5_cex_hide.setObjectName(u"p5_cex_hide")

        self.horizontalLayout_10.addWidget(self.p5_cex_hide)

        self.label_CEX_Top = QLabel(self.frame_20)
        self.label_CEX_Top.setObjectName(u"label_CEX_Top")
        sizePolicy5.setHeightForWidth(self.label_CEX_Top.sizePolicy().hasHeightForWidth())
        self.label_CEX_Top.setSizePolicy(sizePolicy5)
        self.label_CEX_Top.setFont(font1)

        self.horizontalLayout_10.addWidget(self.label_CEX_Top)

        self.p5_cex_info = QPushButton(self.frame_20)
        self.p5_cex_info.setObjectName(u"p5_cex_info")
        sizePolicy.setHeightForWidth(self.p5_cex_info.sizePolicy().hasHeightForWidth())
        self.p5_cex_info.setSizePolicy(sizePolicy)
        self.p5_cex_info.setIcon(icon19)

        self.horizontalLayout_10.addWidget(self.p5_cex_info)


        self.verticalLayout_13.addWidget(self.frame_20)

        self.p5_cex_frame = QFrame(self.p5_fLeft)
        self.p5_cex_frame.setObjectName(u"p5_cex_frame")
        sizePolicy3.setHeightForWidth(self.p5_cex_frame.sizePolicy().hasHeightForWidth())
        self.p5_cex_frame.setSizePolicy(sizePolicy3)
        self.p5_cex_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_cex_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.p5_cex_frame)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.p5_cex_web = QWebEngineView(self.p5_cex_frame)
        self.p5_cex_web.setObjectName(u"p5_cex_web")
        sizePolicy3.setHeightForWidth(self.p5_cex_web.sizePolicy().hasHeightForWidth())
        self.p5_cex_web.setSizePolicy(sizePolicy3)
        self.p5_cex_web.setMinimumSize(QSize(700, 680))
        self.p5_cex_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_21.addWidget(self.p5_cex_web)


        self.verticalLayout_13.addWidget(self.p5_cex_frame)

        self.frame_21 = QFrame(self.p5_fLeft)
        self.frame_21.setObjectName(u"frame_21")
        sizePolicy5.setHeightForWidth(self.frame_21.sizePolicy().hasHeightForWidth())
        self.frame_21.setSizePolicy(sizePolicy5)
        self.frame_21.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.p5_vex_hide = QPushButton(self.frame_21)
        self.p5_vex_hide.setObjectName(u"p5_vex_hide")

        self.horizontalLayout_9.addWidget(self.p5_vex_hide)

        self.label_VEX_Top = QLabel(self.frame_21)
        self.label_VEX_Top.setObjectName(u"label_VEX_Top")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_VEX_Top.sizePolicy().hasHeightForWidth())
        self.label_VEX_Top.setSizePolicy(sizePolicy6)
        self.label_VEX_Top.setFont(font1)

        self.horizontalLayout_9.addWidget(self.label_VEX_Top)

        self.p5_vex_info = QPushButton(self.frame_21)
        self.p5_vex_info.setObjectName(u"p5_vex_info")
        sizePolicy.setHeightForWidth(self.p5_vex_info.sizePolicy().hasHeightForWidth())
        self.p5_vex_info.setSizePolicy(sizePolicy)
        self.p5_vex_info.setIcon(icon19)

        self.horizontalLayout_9.addWidget(self.p5_vex_info)


        self.verticalLayout_13.addWidget(self.frame_21)

        self.p5_vex_frame = QFrame(self.p5_fLeft)
        self.p5_vex_frame.setObjectName(u"p5_vex_frame")
        sizePolicy3.setHeightForWidth(self.p5_vex_frame.sizePolicy().hasHeightForWidth())
        self.p5_vex_frame.setSizePolicy(sizePolicy3)
        self.p5_vex_frame.setMinimumSize(QSize(333, 333))
        self.p5_vex_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_vex_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.p5_vex_frame)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.p5_vex_web = QWebEngineView(self.p5_vex_frame)
        self.p5_vex_web.setObjectName(u"p5_vex_web")
        sizePolicy3.setHeightForWidth(self.p5_vex_web.sizePolicy().hasHeightForWidth())
        self.p5_vex_web.setSizePolicy(sizePolicy3)
        self.p5_vex_web.setMinimumSize(QSize(700, 680))
        self.p5_vex_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_22.addWidget(self.p5_vex_web)


        self.verticalLayout_13.addWidget(self.p5_vex_frame)


        self.horizontalLayout_3.addWidget(self.p5_fLeft)

        self.p5_fMid = QFrame(self.frame_15)
        self.p5_fMid.setObjectName(u"p5_fMid")
        sizePolicy3.setHeightForWidth(self.p5_fMid.sizePolicy().hasHeightForWidth())
        self.p5_fMid.setSizePolicy(sizePolicy3)
        self.p5_fMid.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_fMid.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.p5_fMid)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.frame_22 = QFrame(self.p5_fMid)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.p5_Oi_hide = QPushButton(self.frame_22)
        self.p5_Oi_hide.setObjectName(u"p5_Oi_hide")

        self.horizontalLayout_12.addWidget(self.p5_Oi_hide)

        self.label_OpenInterest_Top = QLabel(self.frame_22)
        self.label_OpenInterest_Top.setObjectName(u"label_OpenInterest_Top")
        sizePolicy5.setHeightForWidth(self.label_OpenInterest_Top.sizePolicy().hasHeightForWidth())
        self.label_OpenInterest_Top.setSizePolicy(sizePolicy5)
        self.label_OpenInterest_Top.setFont(font1)

        self.horizontalLayout_12.addWidget(self.label_OpenInterest_Top)

        self.p5_Oi_info = QPushButton(self.frame_22)
        self.p5_Oi_info.setObjectName(u"p5_Oi_info")
        sizePolicy.setHeightForWidth(self.p5_Oi_info.sizePolicy().hasHeightForWidth())
        self.p5_Oi_info.setSizePolicy(sizePolicy)
        self.p5_Oi_info.setIcon(icon19)

        self.horizontalLayout_12.addWidget(self.p5_Oi_info)


        self.verticalLayout_12.addWidget(self.frame_22)

        self.p5_Oi = QFrame(self.p5_fMid)
        self.p5_Oi.setObjectName(u"p5_Oi")
        sizePolicy3.setHeightForWidth(self.p5_Oi.sizePolicy().hasHeightForWidth())
        self.p5_Oi.setSizePolicy(sizePolicy3)
        self.p5_Oi.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_Oi.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.p5_Oi)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.p5_Oi_web = QWebEngineView(self.p5_Oi)
        self.p5_Oi_web.setObjectName(u"p5_Oi_web")
        sizePolicy3.setHeightForWidth(self.p5_Oi_web.sizePolicy().hasHeightForWidth())
        self.p5_Oi_web.setSizePolicy(sizePolicy3)
        self.p5_Oi_web.setMinimumSize(QSize(700, 680))
        self.p5_Oi_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_23.addWidget(self.p5_Oi_web)


        self.verticalLayout_12.addWidget(self.p5_Oi)

        self.frame_23 = QFrame(self.p5_fMid)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.p5_vol_hide = QPushButton(self.frame_23)
        self.p5_vol_hide.setObjectName(u"p5_vol_hide")

        self.horizontalLayout_4.addWidget(self.p5_vol_hide)

        self.label_Volume_Top = QLabel(self.frame_23)
        self.label_Volume_Top.setObjectName(u"label_Volume_Top")
        sizePolicy5.setHeightForWidth(self.label_Volume_Top.sizePolicy().hasHeightForWidth())
        self.label_Volume_Top.setSizePolicy(sizePolicy5)
        self.label_Volume_Top.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_Volume_Top)

        self.p5_vol_info = QPushButton(self.frame_23)
        self.p5_vol_info.setObjectName(u"p5_vol_info")
        sizePolicy.setHeightForWidth(self.p5_vol_info.sizePolicy().hasHeightForWidth())
        self.p5_vol_info.setSizePolicy(sizePolicy)
        self.p5_vol_info.setIcon(icon19)

        self.horizontalLayout_4.addWidget(self.p5_vol_info)


        self.verticalLayout_12.addWidget(self.frame_23)

        self.p5_Vol = QFrame(self.p5_fMid)
        self.p5_Vol.setObjectName(u"p5_Vol")
        sizePolicy3.setHeightForWidth(self.p5_Vol.sizePolicy().hasHeightForWidth())
        self.p5_Vol.setSizePolicy(sizePolicy3)
        self.p5_Vol.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_Vol.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.p5_Vol)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.p5_Vol_web = QWebEngineView(self.p5_Vol)
        self.p5_Vol_web.setObjectName(u"p5_Vol_web")
        sizePolicy3.setHeightForWidth(self.p5_Vol_web.sizePolicy().hasHeightForWidth())
        self.p5_Vol_web.setSizePolicy(sizePolicy3)
        self.p5_Vol_web.setMinimumSize(QSize(700, 680))
        self.p5_Vol_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_25.addWidget(self.p5_Vol_web)


        self.verticalLayout_12.addWidget(self.p5_Vol)

        self.frame_24 = QFrame(self.p5_fMid)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.p5_VolOi_hide = QPushButton(self.frame_24)
        self.p5_VolOi_hide.setObjectName(u"p5_VolOi_hide")

        self.horizontalLayout_8.addWidget(self.p5_VolOi_hide)

        self.label_VolOi_Top = QLabel(self.frame_24)
        self.label_VolOi_Top.setObjectName(u"label_VolOi_Top")
        sizePolicy6.setHeightForWidth(self.label_VolOi_Top.sizePolicy().hasHeightForWidth())
        self.label_VolOi_Top.setSizePolicy(sizePolicy6)
        self.label_VolOi_Top.setFont(font1)

        self.horizontalLayout_8.addWidget(self.label_VolOi_Top)

        self.p5_VolOi_info = QPushButton(self.frame_24)
        self.p5_VolOi_info.setObjectName(u"p5_VolOi_info")
        sizePolicy.setHeightForWidth(self.p5_VolOi_info.sizePolicy().hasHeightForWidth())
        self.p5_VolOi_info.setSizePolicy(sizePolicy)
        self.p5_VolOi_info.setIcon(icon19)

        self.horizontalLayout_8.addWidget(self.p5_VolOi_info)


        self.verticalLayout_12.addWidget(self.frame_24)

        self.p5_VolOi = QFrame(self.p5_fMid)
        self.p5_VolOi.setObjectName(u"p5_VolOi")
        sizePolicy3.setHeightForWidth(self.p5_VolOi.sizePolicy().hasHeightForWidth())
        self.p5_VolOi.setSizePolicy(sizePolicy3)
        self.p5_VolOi.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_VolOi.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.p5_VolOi)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.p5_VolOi_web = QWebEngineView(self.p5_VolOi)
        self.p5_VolOi_web.setObjectName(u"p5_VolOi_web")
        sizePolicy3.setHeightForWidth(self.p5_VolOi_web.sizePolicy().hasHeightForWidth())
        self.p5_VolOi_web.setSizePolicy(sizePolicy3)
        self.p5_VolOi_web.setMinimumSize(QSize(700, 680))
        self.p5_VolOi_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_24.addWidget(self.p5_VolOi_web)


        self.verticalLayout_12.addWidget(self.p5_VolOi)


        self.horizontalLayout_3.addWidget(self.p5_fMid)

        self.p5_fRight = QFrame(self.frame_15)
        self.p5_fRight.setObjectName(u"p5_fRight")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.p5_fRight.sizePolicy().hasHeightForWidth())
        self.p5_fRight.setSizePolicy(sizePolicy7)
        self.p5_fRight.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_fRight.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.p5_fRight)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.p5_twidget = QFrame(self.p5_fRight)
        self.p5_twidget.setObjectName(u"p5_twidget")
        self.p5_twidget.setFrameShape(QFrame.Shape.NoFrame)
        self.p5_twidget.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.p5_twidget)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.tableWidget_p5 = QTableWidget(self.p5_twidget)
        self.tableWidget_p5.setObjectName(u"tableWidget_p5")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.tableWidget_p5.sizePolicy().hasHeightForWidth())
        self.tableWidget_p5.setSizePolicy(sizePolicy8)

        self.verticalLayout_28.addWidget(self.tableWidget_p5)

        self.frame_49 = QFrame(self.p5_twidget)
        self.frame_49.setObjectName(u"frame_49")
        sizePolicy4.setHeightForWidth(self.frame_49.sizePolicy().hasHeightForWidth())
        self.frame_49.setSizePolicy(sizePolicy4)
        self.frame_49.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_49.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_49)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.p5_VT_button = QPushButton(self.frame_49)
        self.p5_VT_button.setObjectName(u"p5_VT_button")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.p5_VT_button.sizePolicy().hasHeightForWidth())
        self.p5_VT_button.setSizePolicy(sizePolicy9)

        self.gridLayout_9.addWidget(self.p5_VT_button, 0, 0, 1, 1)

        self.p5_GP_button = QPushButton(self.frame_49)
        self.p5_GP_button.setObjectName(u"p5_GP_button")

        self.gridLayout_9.addWidget(self.p5_GP_button, 0, 1, 1, 1)

        self.p5_GTR_button = QPushButton(self.frame_49)
        self.p5_GTR_button.setObjectName(u"p5_GTR_button")

        self.gridLayout_9.addWidget(self.p5_GTR_button, 1, 0, 1, 1)

        self.p5_MC_button = QPushButton(self.frame_49)
        self.p5_MC_button.setObjectName(u"p5_MC_button")

        self.gridLayout_9.addWidget(self.p5_MC_button, 1, 1, 1, 1)


        self.verticalLayout_28.addWidget(self.frame_49)


        self.verticalLayout_26.addWidget(self.p5_twidget)


        self.horizontalLayout_3.addWidget(self.p5_fRight)


        self.verticalLayout_27.addWidget(self.frame_15)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_14.addWidget(self.scrollArea_2)

        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.verticalLayout_8 = QVBoxLayout(self.page_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_4 = QFrame(self.page_6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_42 = QPushButton(self.frame_4)
        self.pushButton_42.setObjectName(u"pushButton_42")
        self.pushButton_42.setIcon(icon)

        self.horizontalLayout_7.addWidget(self.pushButton_42)

        self.pushButton_29 = QPushButton(self.frame_4)
        self.pushButton_29.setObjectName(u"pushButton_29")

        self.horizontalLayout_7.addWidget(self.pushButton_29)

        self.horizontalSpacer_20 = QSpacerItem(809, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_20)


        self.verticalLayout_8.addWidget(self.frame_4)

        self.frame_43 = QFrame(self.page_6)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_43)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.frame_5 = QFrame(self.frame_43)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy5.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy5)
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_5)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.pushButton_31 = QPushButton(self.frame_5)
        self.pushButton_31.setObjectName(u"pushButton_31")
        self.pushButton_31.setCheckable(True)

        self.gridLayout_12.addWidget(self.pushButton_31, 3, 1, 1, 1)

        self.pushButton_28 = QPushButton(self.frame_5)
        self.pushButton_28.setObjectName(u"pushButton_28")
        self.pushButton_28.setCheckable(True)

        self.gridLayout_12.addWidget(self.pushButton_28, 3, 0, 1, 1)

        self.p6_manual_button = QPushButton(self.frame_5)
        self.p6_manual_button.setObjectName(u"p6_manual_button")
        self.p6_manual_button.setIcon(icon17)

        self.gridLayout_12.addWidget(self.p6_manual_button, 1, 0, 1, 1)

        self.p6_interval_toolbutton = QToolButton(self.frame_5)
        self.p6_interval_toolbutton.setObjectName(u"p6_interval_toolbutton")
        self.p6_interval_toolbutton.setIcon(icon16)
        self.p6_interval_toolbutton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.p6_interval_toolbutton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        self.gridLayout_12.addWidget(self.p6_interval_toolbutton, 1, 2, 1, 1)

        self.p6_checkbox = QCheckBox(self.frame_5)
        self.p6_checkbox.setObjectName(u"p6_checkbox")

        self.gridLayout_12.addWidget(self.p6_checkbox, 1, 1, 1, 1)


        self.horizontalLayout_25.addWidget(self.frame_5)

        self.frame_56 = QFrame(self.frame_43)
        self.frame_56.setObjectName(u"frame_56")
        sizePolicy4.setHeightForWidth(self.frame_56.sizePolicy().hasHeightForWidth())
        self.frame_56.setSizePolicy(sizePolicy4)
        self.frame_56.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_56.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_56)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.pushButton_41 = QPushButton(self.frame_56)
        self.pushButton_41.setObjectName(u"pushButton_41")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.pushButton_41.sizePolicy().hasHeightForWidth())
        self.pushButton_41.setSizePolicy(sizePolicy10)

        self.horizontalLayout_30.addWidget(self.pushButton_41)


        self.horizontalLayout_25.addWidget(self.frame_56)

        self.frame_48 = QFrame(self.frame_43)
        self.frame_48.setObjectName(u"frame_48")
        sizePolicy5.setHeightForWidth(self.frame_48.sizePolicy().hasHeightForWidth())
        self.frame_48.setSizePolicy(sizePolicy5)
        self.frame_48.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_48.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_48)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.p6_start_button = QPushButton(self.frame_48)
        self.p6_start_button.setObjectName(u"p6_start_button")
        self.p6_start_button.setIcon(icon15)

        self.gridLayout_4.addWidget(self.p6_start_button, 0, 0, 1, 1)

        self.p6_end_button = QPushButton(self.frame_48)
        self.p6_end_button.setObjectName(u"p6_end_button")
        self.p6_end_button.setIcon(icon18)

        self.gridLayout_4.addWidget(self.p6_end_button, 0, 1, 1, 1)

        self.pushButton_38 = QPushButton(self.frame_48)
        self.pushButton_38.setObjectName(u"pushButton_38")
        self.pushButton_38.setCheckable(True)

        self.gridLayout_4.addWidget(self.pushButton_38, 1, 0, 1, 1)

        self.pushButton_35 = QPushButton(self.frame_48)
        self.pushButton_35.setObjectName(u"pushButton_35")
        self.pushButton_35.setCheckable(True)

        self.gridLayout_4.addWidget(self.pushButton_35, 1, 1, 1, 1)

        self.pushButton_33 = QPushButton(self.frame_48)
        self.pushButton_33.setObjectName(u"pushButton_33")
        self.pushButton_33.setCheckable(True)

        self.gridLayout_4.addWidget(self.pushButton_33, 2, 0, 1, 1)

        self.pushButton_40 = QPushButton(self.frame_48)
        self.pushButton_40.setObjectName(u"pushButton_40")
        self.pushButton_40.setCheckable(True)

        self.gridLayout_4.addWidget(self.pushButton_40, 2, 1, 1, 1)


        self.horizontalLayout_25.addWidget(self.frame_48)

        self.frame_57 = QFrame(self.frame_43)
        self.frame_57.setObjectName(u"frame_57")
        sizePolicy4.setHeightForWidth(self.frame_57.sizePolicy().hasHeightForWidth())
        self.frame_57.setSizePolicy(sizePolicy4)
        self.frame_57.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_57.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_57)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.pushButton_43 = QPushButton(self.frame_57)
        self.pushButton_43.setObjectName(u"pushButton_43")
        sizePolicy10.setHeightForWidth(self.pushButton_43.sizePolicy().hasHeightForWidth())
        self.pushButton_43.setSizePolicy(sizePolicy10)

        self.horizontalLayout_32.addWidget(self.pushButton_43)


        self.horizontalLayout_25.addWidget(self.frame_57)


        self.verticalLayout_8.addWidget(self.frame_43)

        self.frame_6 = QFrame(self.page_6)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.p6_Rframe = QFrame(self.frame_6)
        self.p6_Rframe.setObjectName(u"p6_Rframe")
        self.p6_Rframe.setFrameShape(QFrame.Shape.NoFrame)
        self.p6_Rframe.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_39 = QVBoxLayout(self.p6_Rframe)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.scrollArea_8 = QScrollArea(self.p6_Rframe)
        self.scrollArea_8.setObjectName(u"scrollArea_8")
        self.scrollArea_8.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_8.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_8.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollAreaWidgetContents_8 = QWidget()
        self.scrollAreaWidgetContents_8.setObjectName(u"scrollAreaWidgetContents_8")
        self.scrollAreaWidgetContents_8.setGeometry(QRect(0, -237, 488, 989))
        self.verticalLayout_37 = QVBoxLayout(self.scrollAreaWidgetContents_8)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.frame_54 = QFrame(self.scrollAreaWidgetContents_8)
        self.frame_54.setObjectName(u"frame_54")
        sizePolicy3.setHeightForWidth(self.frame_54.sizePolicy().hasHeightForWidth())
        self.frame_54.setSizePolicy(sizePolicy3)
        self.frame_54.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_54.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_43 = QVBoxLayout(self.frame_54)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.frame_51 = QFrame(self.frame_54)
        self.frame_51.setObjectName(u"frame_51")
        self.frame_51.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_51.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_51)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_41 = QLabel(self.frame_51)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFont(font1)

        self.horizontalLayout_27.addWidget(self.label_41)

        self.horizontalSpacer_40 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_40)

        self.pushButton_30 = QPushButton(self.frame_51)
        self.pushButton_30.setObjectName(u"pushButton_30")

        self.horizontalLayout_27.addWidget(self.pushButton_30)


        self.verticalLayout_43.addWidget(self.frame_51)

        self.tableWidget_12 = QTableWidget(self.frame_54)
        self.tableWidget_12.setObjectName(u"tableWidget_12")
        self.tableWidget_12.setMinimumSize(QSize(450, 175))
        self.tableWidget_12.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_12.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_12.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_12.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_12.setDragEnabled(True)
        self.tableWidget_12.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_12.setSortingEnabled(True)

        self.verticalLayout_43.addWidget(self.tableWidget_12)


        self.verticalLayout_37.addWidget(self.frame_54)

        self.frame_53 = QFrame(self.scrollAreaWidgetContents_8)
        self.frame_53.setObjectName(u"frame_53")
        sizePolicy3.setHeightForWidth(self.frame_53.sizePolicy().hasHeightForWidth())
        self.frame_53.setSizePolicy(sizePolicy3)
        self.frame_53.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_53.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_42 = QVBoxLayout(self.frame_53)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.frame_47 = QFrame(self.frame_53)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_47.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_47)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_38 = QLabel(self.frame_47)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font1)

        self.horizontalLayout_24.addWidget(self.label_38)

        self.horizontalSpacer_34 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_34)

        self.pushButton_34 = QPushButton(self.frame_47)
        self.pushButton_34.setObjectName(u"pushButton_34")

        self.horizontalLayout_24.addWidget(self.pushButton_34)


        self.verticalLayout_42.addWidget(self.frame_47)

        self.tableWidget_10 = QTableWidget(self.frame_53)
        self.tableWidget_10.setObjectName(u"tableWidget_10")
        self.tableWidget_10.setMinimumSize(QSize(450, 300))
        self.tableWidget_10.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_10.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_10.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_10.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_10.setDragEnabled(True)
        self.tableWidget_10.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_10.setSortingEnabled(True)

        self.verticalLayout_42.addWidget(self.tableWidget_10)

        self.frame_50 = QFrame(self.frame_53)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_50.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_50)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_40 = QLabel(self.frame_50)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font1)

        self.horizontalLayout_26.addWidget(self.label_40)

        self.horizontalSpacer_38 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_38)

        self.pushButton_36 = QPushButton(self.frame_50)
        self.pushButton_36.setObjectName(u"pushButton_36")

        self.horizontalLayout_26.addWidget(self.pushButton_36)


        self.verticalLayout_42.addWidget(self.frame_50)

        self.tableWidget_11 = QTableWidget(self.frame_53)
        self.tableWidget_11.setObjectName(u"tableWidget_11")
        self.tableWidget_11.setMinimumSize(QSize(450, 300))
        self.tableWidget_11.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_11.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_11.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_11.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_11.setDragEnabled(True)
        self.tableWidget_11.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_11.setSortingEnabled(True)

        self.verticalLayout_42.addWidget(self.tableWidget_11)


        self.verticalLayout_37.addWidget(self.frame_53)

        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)

        self.verticalLayout_39.addWidget(self.scrollArea_8)


        self.gridLayout_11.addWidget(self.p6_Rframe, 0, 1, 1, 1)

        self.p6_Lframe = QFrame(self.frame_6)
        self.p6_Lframe.setObjectName(u"p6_Lframe")
        self.p6_Lframe.setFrameShape(QFrame.Shape.NoFrame)
        self.p6_Lframe.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.p6_Lframe)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.scrollArea_7 = QScrollArea(self.p6_Lframe)
        self.scrollArea_7.setObjectName(u"scrollArea_7")
        self.scrollArea_7.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_7.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_7.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollAreaWidgetContents_7 = QWidget()
        self.scrollAreaWidgetContents_7.setObjectName(u"scrollAreaWidgetContents_7")
        self.scrollAreaWidgetContents_7.setGeometry(QRect(0, -751, 488, 1446))
        self.verticalLayout_36 = QVBoxLayout(self.scrollAreaWidgetContents_7)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.frame_52 = QFrame(self.scrollAreaWidgetContents_7)
        self.frame_52.setObjectName(u"frame_52")
        sizePolicy3.setHeightForWidth(self.frame_52.sizePolicy().hasHeightForWidth())
        self.frame_52.setSizePolicy(sizePolicy3)
        self.frame_52.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_52.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_41 = QVBoxLayout(self.frame_52)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.frame_36 = QFrame(self.frame_52)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_36.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_34 = QLabel(self.frame_36)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font1)

        self.horizontalLayout_19.addWidget(self.label_34)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_22)


        self.verticalLayout_41.addWidget(self.frame_36)

        self.tableWidget_9 = QTableWidget(self.frame_52)
        self.tableWidget_9.setObjectName(u"tableWidget_9")
        sizePolicy.setHeightForWidth(self.tableWidget_9.sizePolicy().hasHeightForWidth())
        self.tableWidget_9.setSizePolicy(sizePolicy)
        self.tableWidget_9.setMinimumSize(QSize(450, 150))
        self.tableWidget_9.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_9.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_9.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_9.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_9.setDragEnabled(True)
        self.tableWidget_9.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_9.setSortingEnabled(True)

        self.verticalLayout_41.addWidget(self.tableWidget_9)

        self.label_36 = QLabel(self.frame_52)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font1)

        self.verticalLayout_41.addWidget(self.label_36)

        self.tableWidget_13 = QTableWidget(self.frame_52)
        self.tableWidget_13.setObjectName(u"tableWidget_13")
        self.tableWidget_13.setMinimumSize(QSize(450, 150))
        self.tableWidget_13.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.tableWidget_13.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_13.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_13.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_13.setDragEnabled(True)
        self.tableWidget_13.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_13.setSortingEnabled(True)

        self.verticalLayout_41.addWidget(self.tableWidget_13)

        self.frame_42 = QFrame(self.frame_52)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_42.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_42)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_35 = QLabel(self.frame_42)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font1)

        self.horizontalLayout_22.addWidget(self.label_35)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_24)


        self.verticalLayout_41.addWidget(self.frame_42)

        self.tableWidget_4 = QTableWidget(self.frame_52)
        self.tableWidget_4.setObjectName(u"tableWidget_4")
        sizePolicy.setHeightForWidth(self.tableWidget_4.sizePolicy().hasHeightForWidth())
        self.tableWidget_4.setSizePolicy(sizePolicy)
        self.tableWidget_4.setMinimumSize(QSize(450, 150))
        self.tableWidget_4.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_4.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_4.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_4.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_4.setDragEnabled(True)
        self.tableWidget_4.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_4.setSortingEnabled(True)

        self.verticalLayout_41.addWidget(self.tableWidget_4)

        self.frame_46 = QFrame(self.frame_52)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_46.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.frame_46)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_37 = QLabel(self.frame_46)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font1)

        self.horizontalLayout_31.addWidget(self.label_37)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_32)


        self.verticalLayout_41.addWidget(self.frame_46)

        self.tableWidget_8 = QTableWidget(self.frame_52)
        self.tableWidget_8.setObjectName(u"tableWidget_8")
        sizePolicy.setHeightForWidth(self.tableWidget_8.sizePolicy().hasHeightForWidth())
        self.tableWidget_8.setSizePolicy(sizePolicy)
        self.tableWidget_8.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_8.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_8.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_8.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_8.setDragEnabled(True)
        self.tableWidget_8.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_8.setSortingEnabled(True)

        self.verticalLayout_41.addWidget(self.tableWidget_8)


        self.verticalLayout_36.addWidget(self.frame_52)

        self.frame_55 = QFrame(self.scrollAreaWidgetContents_7)
        self.frame_55.setObjectName(u"frame_55")
        sizePolicy3.setHeightForWidth(self.frame_55.sizePolicy().hasHeightForWidth())
        self.frame_55.setSizePolicy(sizePolicy3)
        self.frame_55.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_55.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_44 = QVBoxLayout(self.frame_55)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.frame_44 = QFrame(self.frame_55)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_44)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalSpacer_25 = QSpacerItem(164, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_25)

        self.label_39 = QLabel(self.frame_44)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font1)

        self.horizontalLayout_29.addWidget(self.label_39)

        self.horizontalSpacer_26 = QSpacerItem(163, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_26)

        self.pushButton_37 = QPushButton(self.frame_44)
        self.pushButton_37.setObjectName(u"pushButton_37")

        self.horizontalLayout_29.addWidget(self.pushButton_37)


        self.verticalLayout_44.addWidget(self.frame_44)

        self.tableWidget_6 = QTableWidget(self.frame_55)
        self.tableWidget_6.setObjectName(u"tableWidget_6")
        self.tableWidget_6.setMinimumSize(QSize(450, 300))
        self.tableWidget_6.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_6.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_6.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_6.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_6.setDragEnabled(True)
        self.tableWidget_6.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_6.setSortingEnabled(True)

        self.verticalLayout_44.addWidget(self.tableWidget_6)

        self.frame_45 = QFrame(self.frame_55)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_45.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_45)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_42 = QLabel(self.frame_45)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setFont(font1)

        self.horizontalLayout_28.addWidget(self.label_42)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_29)

        self.pushButton_39 = QPushButton(self.frame_45)
        self.pushButton_39.setObjectName(u"pushButton_39")

        self.horizontalLayout_28.addWidget(self.pushButton_39)


        self.verticalLayout_44.addWidget(self.frame_45)

        self.tableWidget_7 = QTableWidget(self.frame_55)
        self.tableWidget_7.setObjectName(u"tableWidget_7")
        self.tableWidget_7.setMinimumSize(QSize(450, 300))
        self.tableWidget_7.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_7.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_7.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget_7.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget_7.setDragEnabled(True)
        self.tableWidget_7.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tableWidget_7.setSortingEnabled(True)

        self.verticalLayout_44.addWidget(self.tableWidget_7)


        self.verticalLayout_36.addWidget(self.frame_55)

        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_7)

        self.verticalLayout_38.addWidget(self.scrollArea_7)


        self.gridLayout_11.addWidget(self.p6_Lframe, 0, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.frame_6)

        self.stackedWidget.addWidget(self.page_6)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.verticalLayout_15 = QVBoxLayout(self.page_7)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.frame_37 = QFrame(self.page_7)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_37.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_37)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalSpacer_11 = QSpacerItem(271, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_11)

        self.label_17 = QLabel(self.frame_37)
        self.label_17.setObjectName(u"label_17")
        font9 = QFont()
        font9.setFamilies([u"Cambria"])
        font9.setPointSize(13)
        font9.setBold(True)
        font9.setUnderline(True)
        self.label_17.setFont(font9)

        self.horizontalLayout_20.addWidget(self.label_17)

        self.horizontalSpacer_12 = QSpacerItem(271, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_12)


        self.verticalLayout_15.addWidget(self.frame_37)

        self.frame_26 = QFrame(self.page_7)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMinimumSize(QSize(723, 808))
        self.frame_26.setFont(font1)
        self.frame_26.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_26)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.scrollArea = QScrollArea(self.frame_26)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 747, 1408))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_30 = QVBoxLayout(self.tab_6)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.label_21 = QLabel(self.tab_6)
        self.label_21.setObjectName(u"label_21")
        font10 = QFont()
        font10.setPointSize(15)
        font10.setBold(True)
        font10.setUnderline(True)
        self.label_21.setFont(font10)

        self.verticalLayout_30.addWidget(self.label_21)

        self.frame_8 = QFrame(self.tab_6)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy3.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy3)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.frame_8)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.label_28 = QLabel(self.frame_8)
        self.label_28.setObjectName(u"label_28")
        font11 = QFont()
        font11.setPointSize(11)
        font11.setBold(True)
        font11.setUnderline(True)
        self.label_28.setFont(font11)

        self.verticalLayout_32.addWidget(self.label_28)

        self.plainTextEdit_21 = QPlainTextEdit(self.frame_8)
        self.plainTextEdit_21.setObjectName(u"plainTextEdit_21")

        self.verticalLayout_32.addWidget(self.plainTextEdit_21)

        self.label_32 = QLabel(self.frame_8)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font11)

        self.verticalLayout_32.addWidget(self.label_32)

        self.plainTextEdit_19 = QPlainTextEdit(self.frame_8)
        self.plainTextEdit_19.setObjectName(u"plainTextEdit_19")

        self.verticalLayout_32.addWidget(self.plainTextEdit_19)


        self.verticalLayout_30.addWidget(self.frame_8)

        self.label_30 = QLabel(self.tab_6)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font10)

        self.verticalLayout_30.addWidget(self.label_30)

        self.frame = QFrame(self.tab_6)
        self.frame.setObjectName(u"frame")
        sizePolicy3.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy3)
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.frame)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.label_19 = QLabel(self.frame)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font11)

        self.verticalLayout_29.addWidget(self.label_19)

        self.plainTextEdit_7 = QPlainTextEdit(self.frame)
        self.plainTextEdit_7.setObjectName(u"plainTextEdit_7")

        self.verticalLayout_29.addWidget(self.plainTextEdit_7)

        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font11)

        self.verticalLayout_29.addWidget(self.label_7)

        self.plainTextEdit_11 = QPlainTextEdit(self.frame)
        self.plainTextEdit_11.setObjectName(u"plainTextEdit_11")

        self.verticalLayout_29.addWidget(self.plainTextEdit_11)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font11)

        self.verticalLayout_29.addWidget(self.label_8)

        self.plainTextEdit_8 = QPlainTextEdit(self.frame)
        self.plainTextEdit_8.setObjectName(u"plainTextEdit_8")

        self.verticalLayout_29.addWidget(self.plainTextEdit_8)


        self.verticalLayout_30.addWidget(self.frame)

        self.label_26 = QLabel(self.tab_6)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font10)

        self.verticalLayout_30.addWidget(self.label_26)

        self.frame_12 = QFrame(self.tab_6)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy3.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy3)
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plainTextEdit_6 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_6.setObjectName(u"plainTextEdit_6")

        self.gridLayout.addWidget(self.plainTextEdit_6, 7, 0, 1, 1)

        self.plainTextEdit_3 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_3.setObjectName(u"plainTextEdit_3")

        self.gridLayout.addWidget(self.plainTextEdit_3, 1, 0, 1, 1)

        self.plainTextEdit_4 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_4.setObjectName(u"plainTextEdit_4")

        self.gridLayout.addWidget(self.plainTextEdit_4, 3, 0, 1, 1)

        self.label_6 = QLabel(self.frame_12)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font11)

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.label_16 = QLabel(self.frame_12)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font11)

        self.gridLayout.addWidget(self.label_16, 2, 1, 1, 1)

        self.plainTextEdit_9 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_9.setObjectName(u"plainTextEdit_9")

        self.gridLayout.addWidget(self.plainTextEdit_9, 1, 1, 1, 1)

        self.plainTextEdit_10 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_10.setObjectName(u"plainTextEdit_10")

        self.gridLayout.addWidget(self.plainTextEdit_10, 5, 1, 1, 1)

        self.label_23 = QLabel(self.frame_12)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font11)

        self.gridLayout.addWidget(self.label_23, 0, 1, 1, 1)

        self.label_20 = QLabel(self.frame_12)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font11)

        self.gridLayout.addWidget(self.label_20, 4, 1, 1, 1)

        self.plainTextEdit_5 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_5.setObjectName(u"plainTextEdit_5")

        self.gridLayout.addWidget(self.plainTextEdit_5, 5, 0, 1, 1)

        self.plainTextEdit_14 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_14.setObjectName(u"plainTextEdit_14")

        self.gridLayout.addWidget(self.plainTextEdit_14, 3, 1, 1, 1)

        self.label_24 = QLabel(self.frame_12)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font11)

        self.gridLayout.addWidget(self.label_24, 6, 1, 1, 1)

        self.label_4 = QLabel(self.frame_12)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font11)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_5 = QLabel(self.frame_12)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font11)

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.plainTextEdit_13 = QPlainTextEdit(self.frame_12)
        self.plainTextEdit_13.setObjectName(u"plainTextEdit_13")

        self.gridLayout.addWidget(self.plainTextEdit_13, 7, 1, 1, 1)

        self.label_3 = QLabel(self.frame_12)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font11)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)


        self.verticalLayout_30.addWidget(self.frame_12)

        self.label_33 = QLabel(self.tab_6)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font10)

        self.verticalLayout_30.addWidget(self.label_33)

        self.frame_2 = QFrame(self.tab_6)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.frame_2)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.label_25 = QLabel(self.frame_2)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font11)

        self.verticalLayout_31.addWidget(self.label_25)

        self.plainTextEdit_2 = QPlainTextEdit(self.frame_2)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")

        self.verticalLayout_31.addWidget(self.plainTextEdit_2)

        self.label_27 = QLabel(self.frame_2)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font11)

        self.verticalLayout_31.addWidget(self.label_27)

        self.plainTextEdit_16 = QPlainTextEdit(self.frame_2)
        self.plainTextEdit_16.setObjectName(u"plainTextEdit_16")

        self.verticalLayout_31.addWidget(self.plainTextEdit_16)

        self.label_31 = QLabel(self.frame_2)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font11)

        self.verticalLayout_31.addWidget(self.label_31)

        self.plainTextEdit_15 = QPlainTextEdit(self.frame_2)
        self.plainTextEdit_15.setObjectName(u"plainTextEdit_15")

        self.verticalLayout_31.addWidget(self.plainTextEdit_15)

        self.label_29 = QLabel(self.frame_2)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font11)

        self.verticalLayout_31.addWidget(self.label_29)

        self.plainTextEdit_20 = QPlainTextEdit(self.frame_2)
        self.plainTextEdit_20.setObjectName(u"plainTextEdit_20")

        self.verticalLayout_31.addWidget(self.plainTextEdit_20)


        self.verticalLayout_30.addWidget(self.frame_2)

        self.tabWidget.addTab(self.tab_6, "")

        self.gridLayout_6.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_7.addWidget(self.scrollArea)


        self.verticalLayout_15.addWidget(self.frame_26)

        self.stackedWidget.addWidget(self.page_7)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.verticalLayout_35.addWidget(self.RightMain)

        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)

        self.horizontalLayout_6.addWidget(self.scrollArea_6)


        self.verticalLayout_6.addWidget(self.MidMainCentral)

        self.BottomMain = QFrame(self.subCentral)
        self.BottomMain.setObjectName(u"BottomMain")
        self.BottomMain.setFrameShape(QFrame.Shape.NoFrame)
        self.BottomMain.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.BottomMain)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_22 = QLabel(self.BottomMain)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_18.addWidget(self.label_22)


        self.verticalLayout_6.addWidget(self.BottomMain)


        self.horizontalLayout.addWidget(self.subCentral)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.CC_button.setDefault(False)
        self.DOC_button.setDefault(False)
        self.stackedWidget.setCurrentIndex(0)
        self.pushButton_20.setDefault(False)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.collapse_leftframe_button.setText("")
        self.pushButton_32.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"CB Charts: FlowLock  v.01", None))
        self.minimizebutton.setText("")
        self.maxbutton.setText("")
        self.closebutton.setText("")
        self.CC_button.setText(QCoreApplication.translate("MainWindow", u"Command Center", None))
        self.SV_button.setText(QCoreApplication.translate("MainWindow", u"Single-View", None))
        self.TV_button.setText(QCoreApplication.translate("MainWindow", u"Tri-View", None))
        self.OW_button.setText(QCoreApplication.translate("MainWindow", u"Overwatch", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Numbers Game", None))
        self.DOC_button.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.toolButton_5.setText(QCoreApplication.translate("MainWindow", u"Indicator", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Disable PopUp", None))
        self.pushButton_44.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pushButton_45.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.pushButton_46.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Journal", None))
        self.clear_notes_button.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.np_edit_button.setText("")
        self.np_new_button.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.np_next_button.setText("")
        self.np_prev_button.setText("")
        self.np_save_button.setText("")
        self.np_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Notepad", None))
        self.p2_startWrap_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.p2_endWrap_button.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Schwab API", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"AppKey", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Paste Redirect URL Here", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Uri", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Secret Key", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.p2_iv_toolbutton.setText(QCoreApplication.translate("MainWindow", u"IV Method", None))
        self.p2_vt_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Volume Tracker", None))
        self.p2_ec_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Extreme CEX", None))
        self.p2_pop_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Pop-Ups", None))
        self.p2_eg_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Extreme GEX", None))
        self.p2_ev_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Extreme VEX", None))
        self.p2_ed_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Extreme DEX", None))
        self.p2_auth_button.setText(QCoreApplication.translate("MainWindow", u"Authenticate", None))
        self.p2_getToken_button.setText(QCoreApplication.translate("MainWindow", u"Get Token", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Alerts", None))
#if QT_CONFIG(whatsthis)
        self.p2_exp_toolbutton.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>1. 0DTE - only todays options. Best for day-traders<br/>2. 1DTE - today and tomorrows options<br/>3. EoW - All options till the end of week. Worth monitoring for Weekly Hedge Pressure<br/>3. EoM - All options through the end of month. Worth monitoring for Monthly Hedge Pressure</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.p2_exp_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Strike Range", None))
#if QT_CONFIG(tooltip)
        self.p2_interval_toolbutton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Auto-Refresh API calls. Set the frequency of data retrieval.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.p2_interval_toolbutton.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Auto-Refresh API calls. Set the frequency of data retrieval.</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.p2_interval_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Refresh Data Intervals", None))
        self.p2_index_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Index", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Command Center", None))
        self.p2_kClean_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Keep \"Clean\" Data", None))
        self.clearCache_button.setText(QCoreApplication.translate("MainWindow", u"Clear Cache", None))
        self.clearNotes_button.setText(QCoreApplication.translate("MainWindow", u"Clear Notes", None))
        self.clearHist_toolbutton.setText(QCoreApplication.translate("MainWindow", u"Clear Historical Data", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Auto-Refresh", None))
        self.p3_startRe_button.setText("")
        self.p3_interval_drop.setText("")
        self.p3_refresh_button.setText("")
        self.p3_endRe_button.setText("")
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Page Control", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"Expiration Range", None))
        self.toolButton_index_p3.setText(QCoreApplication.translate("MainWindow", u"Index", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Universal Settings", None))
        self.toolButton_4.setText(QCoreApplication.translate("MainWindow", u"Chart", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Full Send", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Exposure Models", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"IV Model", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Full Send", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Vol/Oi Models", None))
        self.toolButton_10.setText(QCoreApplication.translate("MainWindow", u"Volume and Open Interest", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Auto-Refresh Page", None))
        self.p4_interval_button.setText(QCoreApplication.translate("MainWindow", u"Intervals", None))
        self.p4_start_button.setText("")
        self.p4_end_button.setText("")
        self.p4_refresh_button.setText("")
        self.p4_hideL_button.setText(QCoreApplication.translate("MainWindow", u"Hide Left Frame", None))
        self.p4_hideR_button.setText(QCoreApplication.translate("MainWindow", u"Hide Right Frame", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Table Flip", None))
        self.p4_v1_drop.setText(QCoreApplication.translate("MainWindow", u"View 1", None))
        self.p4_v2_drop.setText(QCoreApplication.translate("MainWindow", u"View 2", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Guesstimate Premium", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"Market Calendar", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Greek Totals/Ratios", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Vol Tracker", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.p4_v3_drop.setText(QCoreApplication.translate("MainWindow", u"View 3", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Guesstimate Premium", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Market Calendar", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Greek Totals/Ratios", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Vol Tracker", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Overwatch", None))
        self.pushButton_24.setText(QCoreApplication.translate("MainWindow", u"EoM", None))
        self.p5_hideC2.setText(QCoreApplication.translate("MainWindow", u"Hide Column 2", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Index", None))
        self.pushButton_20.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.p5_interval_toolbutton.setText("")
        self.pushButton_19.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Auto-Refresh Page", None))
        self.p5_start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.p5_hideC1.setText(QCoreApplication.translate("MainWindow", u"Hide Column 1", None))
        self.p5_hideC3.setText(QCoreApplication.translate("MainWindow", u"Hide Column 3", None))
        self.p5_manual_button.setText("")
        self.pushButton_21.setText(QCoreApplication.translate("MainWindow", u"0DTE", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"Frame Control", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"Expiration", None))
        self.pushButton_22.setText(QCoreApplication.translate("MainWindow", u"1DTE", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"IV Method", None))
        self.p5_end_button.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.pushButton_23.setText(QCoreApplication.translate("MainWindow", u"EoW", None))
        self.pushButton_25.setText(QCoreApplication.translate("MainWindow", u"Brent Black Scholes", None))
        self.pushButton_26.setText(QCoreApplication.translate("MainWindow", u"Grok", None))
        self.pushButton_27.setText(QCoreApplication.translate("MainWindow", u"Hybrid_one", None))
        self.p5_gex_hide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_GEX_Top.setText(QCoreApplication.translate("MainWindow", u"GEX", None))
        self.p5_gex_info.setText("")
        self.p5_dex_hide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_DEX_Top.setText(QCoreApplication.translate("MainWindow", u"DEX", None))
        self.p5_dex_info.setText("")
        self.p5_cex_hide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_CEX_Top.setText(QCoreApplication.translate("MainWindow", u"CEX", None))
        self.p5_cex_info.setText("")
        self.p5_vex_hide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_VEX_Top.setText(QCoreApplication.translate("MainWindow", u"VEX", None))
        self.p5_vex_info.setText("")
        self.p5_Oi_hide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_OpenInterest_Top.setText(QCoreApplication.translate("MainWindow", u"Open Interest", None))
        self.p5_Oi_info.setText("")
        self.p5_vol_hide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_Volume_Top.setText(QCoreApplication.translate("MainWindow", u"Volume", None))
        self.p5_vol_info.setText("")
        self.p5_VolOi_hide.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.label_VolOi_Top.setText(QCoreApplication.translate("MainWindow", u"Vol/Open Interest", None))
        self.p5_VolOi_info.setText("")
        self.p5_VT_button.setText(QCoreApplication.translate("MainWindow", u"Vol Tracker", None))
        self.p5_GP_button.setText(QCoreApplication.translate("MainWindow", u"GP Track", None))
        self.p5_GTR_button.setText(QCoreApplication.translate("MainWindow", u"Greek T/R", None))
        self.p5_MC_button.setText(QCoreApplication.translate("MainWindow", u"Market Cal", None))
        self.pushButton_42.setText("")
        self.pushButton_29.setText(QCoreApplication.translate("MainWindow", u"PopOut", None))
        self.pushButton_31.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.pushButton_28.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.p6_manual_button.setText("")
        self.p6_interval_toolbutton.setText("")
        self.p6_checkbox.setText(QCoreApplication.translate("MainWindow", u"Auto-Refresh Page", None))
        self.pushButton_41.setText(QCoreApplication.translate("MainWindow", u"\u2560", None))
        self.p6_start_button.setText("")
        self.p6_end_button.setText("")
        self.pushButton_38.setText(QCoreApplication.translate("MainWindow", u"\u2554", None))
        self.pushButton_35.setText(QCoreApplication.translate("MainWindow", u"\u2557", None))
        self.pushButton_33.setText(QCoreApplication.translate("MainWindow", u"\u2559", None))
        self.pushButton_40.setText(QCoreApplication.translate("MainWindow", u"\u255d", None))
        self.pushButton_43.setText(QCoreApplication.translate("MainWindow", u"\u2563", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Market Calendar", None))
        self.pushButton_30.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Full", None))
        self.pushButton_34.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"*Top 50 Premium Blocks", None))
        self.pushButton_36.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Greek Totals", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Greek Rank", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Greek Ratios", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"P/C", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"0DTE", None))
        self.pushButton_37.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"*Top 50 Premium Blocks (0DTE)", None))
        self.pushButton_39.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Index", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"SPX", None))
        self.plainTextEdit_21.setPlainText("")
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"NDX", None))
        self.plainTextEdit_19.setPlainText("")
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"IV Models", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Hybrid_one", None))
        self.plainTextEdit_7.setPlainText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Brent Black Scholes", None))
        self.plainTextEdit_11.setPlainText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Grok", None))
        self.plainTextEdit_8.setPlainText("")
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Greeks", None))
        self.plainTextEdit_6.setPlainText("")
        self.plainTextEdit_3.setPlainText("")
        self.plainTextEdit_4.setPlainText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Vanna", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Delta Exposure (DEX)", None))
        self.plainTextEdit_9.setPlainText("")
        self.plainTextEdit_10.setPlainText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Gamma Exposure (GEX)", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Charm Exposure (CEX)", None))
        self.plainTextEdit_5.setPlainText("")
        self.plainTextEdit_14.setPlainText("")
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Vanna Exposure (VEX)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Delta", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Charm", None))
        self.plainTextEdit_13.setPlainText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Gamma", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"TimeFrames", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"0DTE", None))
        self.plainTextEdit_2.setPlainText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"1DTE", None))
        self.plainTextEdit_16.setPlainText("")
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"EoW", None))
        self.plainTextEdit_15.setPlainText("")
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"EoM", None))
        self.plainTextEdit_20.setPlainText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Info", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Powered by The Camels of Wallstreet", None))
    # retranslateUi

