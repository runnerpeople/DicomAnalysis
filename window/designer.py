#!python
# -*- coding: utf-8 -*-


# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import window.resources

from PyQt4.QtCore import QEvent, QObject, pyqtSignal

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

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
        MainWindow.setFixedSize(445, 505)
        MainWindow.setStyleSheet(_fromUtf8("#MainWindow { background-image: url(:/image/497102554.jpg); }"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(-1, -1, 451, 511))
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 140, 411, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.username_label = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_label.sizePolicy().hasHeightForWidth())
        self.username_label.setSizePolicy(sizePolicy)
        self.username_label.setMinimumSize(QtCore.QSize(100, 0))
        self.username_label.setStyleSheet(_fromUtf8("#username_label { color : white; }"))
        self.username_label.setObjectName(_fromUtf8("username_label"))
        self.horizontalLayout.addWidget(self.username_label)
        self.username_edit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_edit.sizePolicy().hasHeightForWidth())
        self.username_edit.setSizePolicy(sizePolicy)
        self.username_edit.setMinimumSize(QtCore.QSize(300, 20))
        self.username_edit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.username_edit.setObjectName(_fromUtf8("username_edit"))
        self.horizontalLayout.addWidget(self.username_edit, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 200, 411, 51))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.password_label = QtGui.QLabel(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_label.sizePolicy().hasHeightForWidth())
        self.password_label.setSizePolicy(sizePolicy)
        self.password_label.setMinimumSize(QtCore.QSize(100, 0))
        self.password_label.setStyleSheet(_fromUtf8("#password_label { color : white; }"))
        self.password_label.setObjectName(_fromUtf8("password_label"))
        self.horizontalLayout_2.addWidget(self.password_label)
        self.password_edit = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.password_edit.setEchoMode(QtGui.QLineEdit.Password)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_edit.sizePolicy().hasHeightForWidth())
        self.password_edit.setSizePolicy(sizePolicy)
        self.password_edit.setMinimumSize(QtCore.QSize(300, 20))
        self.password_edit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.password_edit.setObjectName(_fromUtf8("password_edit"))
        self.horizontalLayout_2.addWidget(self.password_edit)
        self.sign_in_button = QtGui.QPushButton(self.groupBox)
        self.sign_in_button.setGeometry(QtCore.QRect(20, 270, 411, 27))
        self.sign_in_button.setStyleSheet(_fromUtf8("#sign_in_button{ background-color : darkBlue;color : white; }"))
        self.sign_in_button.setCheckable(False)
        self.sign_in_button.setChecked(False)
        self.sign_in_button.setObjectName(_fromUtf8("sign_in_button"))
        self.sign_up_label = QtGui.QLabel(self.groupBox)
        self.sign_up_label.setGeometry(QtCore.QRect(20, 470, 171, 31))
        self.sign_up_label.setObjectName(_fromUtf8("sign_up_label"))
        self.sign_up_label.setStyleSheet(_fromUtf8("#sign_up_label { color : white; }"))
        self.forgot_password_label = QtGui.QLabel(self.groupBox)
        self.forgot_password_label.setGeometry(QtCore.QRect(270, 470, 161, 31))
        self.forgot_password_label.setObjectName(_fromUtf8("forgot_password_label"))
        self.forgot_password_label.setStyleSheet(_fromUtf8("#forgot_password_label { color : white; }"))
        self.forgot_password_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 454, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "DicomAnalysis", None))
        self.username_label.setText(_translate("MainWindow", "Username", None))
        self.password_label.setText(_translate("MainWindow", "Password", None))
        self.sign_in_button.setText(_translate("MainWindow", "Sign In", None))
        self.sign_up_label.setText(_translate("MainWindow", "No account yet? Create one", None))
        self.forgot_password_label.setText(_translate("MainWindow", "Forgot password?", None))