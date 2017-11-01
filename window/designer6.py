# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\\PyCharmProjects\\Dicom_database\\ui\\db_url.ui'
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
        self.confirm_button = QtGui.QPushButton(self.centralwidget)
        self.confirm_button.setGeometry(QtCore.QRect(150, 90, 93, 28))
        self.confirm_button.setStyleSheet(_fromUtf8("#confirm_button{ background-color : darkBlue;color : white; }"))
        self.confirm_button.setObjectName(_fromUtf8("confirm_button"))
        self.info_label = QtGui.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(10, 10, 251, 20))
        self.info_label.setStyleSheet(_fromUtf8("#info_label { color : white; }"))
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setObjectName(_fromUtf8("info_label"))
        self.url_edit = QtGui.QLineEdit(self.centralwidget)
        self.url_edit.setGeometry(QtCore.QRect(20, 50, 231, 22))
        self.url_edit.setObjectName(_fromUtf8("url_edit"))
        self.check_button = QtGui.QPushButton(self.centralwidget)
        self.check_button.setGeometry(QtCore.QRect(20, 90, 93, 28))
        self.check_button.setStyleSheet(_fromUtf8("#check_button{ background-color : darkBlue;color : white; }"))
        self.check_button.setObjectName(_fromUtf8("check_button"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.confirm_button.setText(_translate("MainWindow", "Confirm", None))
        self.info_label.setText(_translate("MainWindow", "Input a URL where MongoDB is deployed", None))
        self.check_button.setText(_translate("MainWindow", "Check", None))

