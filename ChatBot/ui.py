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
        TabWidget.resize(1280, 720)
        self.TabWidget = TabWidget
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.scrollArea = QtWidgets.QScrollArea(self.tab)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 1231, 451))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1229, 449))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser_2.setGeometry(QtCore.QRect(0, 0, 1211, 451))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar.setGeometry(QtCore.QRect(1210, 0, 16, 451))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab)
        self.scrollArea_2.setGeometry(QtCore.QRect(20, 489, 1151, 181))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1149, 179))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 1161, 181))
        self.textEdit.setObjectName("textEdit")
        self.verticalScrollBar_2 = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_2)
        self.verticalScrollBar_2.setGeometry(QtCore.QRect(1130, 0, 16, 181))
        self.verticalScrollBar_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_2.setObjectName("verticalScrollBar_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(1180, 490, 71, 181))
        self.pushButton.clicked.connect(self.sendMessageUser)
        self.pushButton.setShortcut('alt')
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        TabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_2 = QtWidgets.QLabel(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 233, 300, 55))
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        self.comboBox.activated.connect(self.setFontFamily)
        self.comboBox.setGeometry(QtCore.QRect(660, 233, 300, 55))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Arial', 'Courier New', 'TimesNewRoman'])

        self.pushButton_3 = QtWidgets.QLabel(self.tab_2)
        # self.pushButton_3.clicked.connect(self.setFontSize)
        self.pushButton_3.setGeometry(QtCore.QRect(340, 133, 300, 55))
        self.pushButton_3.setObjectName("pushButton_3")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_2.activated.connect(self.setFontSize)
        self.comboBox_2.setGeometry(QtCore.QRect(660, 133, 300, 55))
        self.comboBox_2.setObjectName("comboBox")
        self.comboBox_2.addItems(
            ['8', '10', '12', '14', '16', '18', '20', '22'])
        self.comboBox_2.setCurrentIndex(2)

        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.clicked.connect(self.setlogo)
        self.pushButton_4.setGeometry(QtCore.QRect(340, 333, 620, 55))
        self.pushButton_4.setObjectName("pushButton_4")
        TabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser.setGeometry(QtCore.QRect(25, 90, 1221, 201))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(600, 30, 80, 40))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(480, 440, 620, 40))
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
        TabWidget.setWindowTitle(_translate("TabWidget", "CSC3180 Project Chat Bot"))
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
    def setFontFamily(self):
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
        self.textEdit.clear()
        # Add text to the box
        self.textBrowser_2.append('Me: \n{}'.format(text))
        # Move cursor to the end
        self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().End)
        # TODO: send the user input to AI

    # TODO: AI sends output to here
    def sendMessageBot(self, text):
        # Add text to the box
        self.textBrowser_2.append('Bot: \n{}'.format(text))
        # Move cursor to the end
        self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().End)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_TabWidget()
    ex.show()
    ex.setFontSize()
    app.exec_()
