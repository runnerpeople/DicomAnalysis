# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\\PyCharmProjects\\Dicom_database\\ui\\about.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setFixedSize(266, 139)
        MainWindow.setStyleSheet(_fromUtf8("#MainWindow { \n"
"    background-image: url(:/image/497102554.jpg);\n"
"}"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.info_label = QtGui.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(10, 10, 251, 121))
        self.info_label.setStyleSheet(_fromUtf8("#info_label { color : white; }"))
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setObjectName(_fromUtf8("info_label"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.info_label.setText(_translate("MainWindow", "DicomAnalysis (v 1.0.0) for Python3\n"
" Program, which enable edit image and \n"
" get information in DICOM files.\n"
"BMSTU IU9-62.\n"
"George Ivanov \n"
"2017", None))

