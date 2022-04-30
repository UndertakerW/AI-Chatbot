# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import json
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QFontDialog, QLabel, QFileDialog
from system_hotkey import SystemHotkey


class Ui_TabWidget(QtWidgets.QTabWidget):
    sig_keyhot = pyqtSignal(str)

    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, TabWidget):
        # self.setWindowIcon(QIcon('logo.jpg'))
        # self.show()
        self.lab = QLabel('Logo', self)
        self.lab.setGeometry(0, 50, 50, 50)
        pixmap = QPixmap('logo.jpg').scaled(50, 50)
        self.lab.setPixmap(pixmap)
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(658, 505)
        self.TabWidget = TabWidget
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_2.setGeometry(QtCore.QRect(50, 0, 551, 271))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setGeometry(QtCore.QRect(50, 300, 551, 81))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.clicked.connect(self.sendMessageUser)
        self.pushButton.setShortcut('alt')
        self.pushButton.setGeometry(QtCore.QRect(520, 430, 75, 23))
        self.pushButton.setObjectName("pushButton")
        TabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_2 = QtWidgets.QLabel(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 60, 150, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        self.comboBox.activated.connect(self.setFont)
        self.comboBox.setGeometry(QtCore.QRect(310, 60, 91, 23))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Arial', 'Courier New', 'TimesNewRoman'])

        self.pushButton_3 = QtWidgets.QLabel(self.tab_2)
        # self.pushButton_3.clicked.connect(self.setFontSize)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 130,  150, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_2.activated.connect(self.setFontSize)
        self.comboBox_2.setGeometry(QtCore.QRect(310, 130, 91, 23))
        self.comboBox_2.setObjectName("comboBox")
        self.comboBox_2.addItems(
            ['6', '8', '10', '12', '14', '16', '18', '20', '22', '24'])

        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.clicked.connect(self.setlogo)
        self.pushButton_4.setGeometry(QtCore.QRect(200, 210, 91, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        TabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser.setGeometry(QtCore.QRect(180, 90, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(270, 50, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(500, 440, 131, 20))
        self.label_2.setObjectName("label_2")
        TabWidget.addTab(self.tab_3, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def setlogo(self):
        filename = QFileDialog.getOpenFileNames(
            self, 'Select an image', os.getcwd(), "All Files(*);;Text Files(*.txt)")
        print(filename)
        pixmap = QPixmap(filename[0][0]).scaled(50, 50)
        self.lab.setPixmap(pixmap)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.pushButton.setText(_translate("TabWidget", "Send"))

        TabWidget.setTabText(TabWidget.indexOf(self.tab),
                             _translate("TabWidget", "CHAT"))
        self.pushButton_2.setText(_translate("TabWidget", "Set Font"))

        self.pushButton_3.setText(_translate("TabWidget", "Set Font Size"))

        self.pushButton_4.setText(_translate("TabWidget", "Set Avatar"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2),
                             _translate("TabWidget", "SET"))
        self.textBrowser.setHtml(_translate("TabWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> Developed by Mingzhuo Yang (118020068), Wei Wu (118010335), and Tao Pan (119010239) </p></body></html>"))
        self.label.setText(_translate("TabWidget", "About"))
        self.label_2.setText(_translate(
            "TabWidget", "CSC3180 Project - Chat Bot"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_3),
                             _translate("TabWidget", "INFO"))

        # Set Font
    def setFont(self):
        text = self.comboBox.currentText()
        fontDict = {'Arial': 'Arial', 'Courier New': 'Courier New',
                    'TimesNewRoman': 'TimesNewRoman'}
        font = QtGui.QFont()
        font.setFamily(fontDict[text])
        self.TabWidget.setFont(font)

    def setFontSize(self):
        text = self.comboBox_2.currentText()
        font = QtGui.QFont()
        font.setPointSize(int(text))
        self.TabWidget.setFont(font)

    def sendMessageUser(self):
        text = self.textEdit.toPlainText()
        # Add text to the box
        self.textBrowser_2.append('Me: {}'.format(text))
        # Move cursor to the end
        self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().End)
        # TODO: send the user input to AI

    # TODO: AI sends output to here
    def sendMessageBot(self, text):
        # Add text to the box
        self.textBrowser_2.append('Bot: {}'.format(text))
        # Move cursor to the end
        self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().End)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_TabWidget()
    ex.show()
    app.exec_()
