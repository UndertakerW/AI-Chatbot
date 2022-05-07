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

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QFontDialog, QLabel, QFileDialog, QSizePolicy
from PyQt5.QtCore import QFileInfo, QCoreApplication

from search import searchKeyword
from search import botSearchKeyword
from filter import filterEmail
from affairscheduler import schedule
from threading import Thread
import threading
import ctypes
import time

import pickle
import numpy as np
import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from keras.models import load_model
import speech_recognition as sr
import csv


class uiThread(QtCore.QThread):
    output = QtCore.pyqtSignal(str)

    def run(self):
        # do something
        return

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

class uiThreadSearch(uiThread):

    def __init__(self, ui, text):
        uiThread.__init__(self)
        self.ui = ui
        self.text = text

    def run(self):
        try:
            result = botSearchKeyword(self.ui, self.text)
            self.output.emit(result)
        except:
            result = 'We are having trouble communicating with Google, \
                please check your internet connection or try again later.'
            self.output.emit(result)
      
class uiThreadEmailFilter(uiThread):

    def __init__(self, ui, text):
        uiThread.__init__(self)
        self.ui = ui
        self.text = text

    def run(self):
        try:
            result = filterEmail(self.ui, self.text)
            self.output.emit(result)
        except:
            result = '''We are having trouble filtering the email,
                please try again later.'''
            self.output.emit(result)  
            
class uiThreadAffairScheduler(uiThread):

    def __init__(self, ui, text):
        uiThread.__init__(self)
        self.ui = ui
        self.text = text

    def run(self):
        try:
            result = schedule(self.ui, self.text)
            self.output.emit(result)
        except:
            result = '''We are having trouble loading scheduler,
                please try again later.'''
            self.output.emit(result)

class Ui_TabWidget(QtWidgets.QTabWidget):
    sig_keyhot = pyqtSignal(str)
    bot_output = pyqtSignal(str)

    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        self.root = QFileInfo(__file__).absolutePath()
        self.setupUi(self)
        self.retranslateUi(self)
        self.dialog_id = 0
        self.email_id = 0
        self.msgBoxes = list()
        self.emailBoxes = list()
        self.avatar = QPixmap(self.root + '\\avatar.ico')
        self.avatarBot = QPixmap(self.root + '\\avatarBot.ico')
        self.ch = Chatter(self)
        self.audio = None
        self.r = sr.Recognizer()
        self.max_n_emails=50


    def setupUi(self, TabWidget):
        self.setWindowIcon(QIcon(self.root+'\\logo.ico'))
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(1280, 720)
        self.TabWidget = TabWidget
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.scrollArea = QtWidgets.QScrollArea(self.tab)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 1240, 451))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1240, 451))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(
                self.scrollToBottomChatBox, QtCore.Qt.UniqueConnection)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab)
        self.scrollArea_2.setGeometry(QtCore.QRect(20, 489, 1130, 181))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1130, 181))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 1131, 181))
        self.textEdit.setObjectName("textEdit")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(1150, 551, 110, 120))
        self.pushButton.clicked.connect(self.sendMessageUserFromTextEdit)
        self.pushButton.setShortcut('alt')
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_speak = QtWidgets.QPushButton(self.tab)
        self.pushButton_speak.setGeometry(QtCore.QRect(1150, 490, 110, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_speak.setFont(font)
        self.pushButton_speak.setObjectName("pushButton_speak")
        self.pushButton_speak.clicked.connect(self.startVoiceRecording)
        # self.pushButton_speak.released.connect(self.endVoiceRecording)
        # self.verticalScrollBar = QtWidgets.QScrollBar(self.scrollArea)
        # self.verticalScrollBar.setGeometry(QtCore.QRect(1250, 40, 16, 160))
        # self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        # self.verticalScrollBar.setObjectName("verticalScrollBar")
        TabWidget.addTab(self.tab, "")

        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.scrollAreaEmail = QtWidgets.QScrollArea(self.tab_4)
        self.scrollAreaEmail.setGeometry(QtCore.QRect(20, 20, 1240, 550))
        self.scrollAreaEmail.setWidgetResizable(True)
        self.scrollAreaEmail.setObjectName("scrollAreaEmail")
        self.scrollAreaEmailWidgetContents = QtWidgets.QWidget()
        self.scrollAreaEmailWidgetContents.setGeometry(QtCore.QRect(0, 0, 1240, 451))
        self.scrollAreaEmailWidgetContents.setObjectName("scrollAreaEmailWidgetContents")
        self.scrollAreaEmail.setWidget(self.scrollAreaEmailWidgetContents)
        self.verticalLayoutEmail = QtWidgets.QVBoxLayout(self.scrollAreaEmailWidgetContents)
        self.verticalLayoutEmail.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutEmail.setObjectName("verticalLayoutEmail")
        self.verticalLayoutEmail.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayoutEmail.setAlignment(QtCore.Qt.AlignTop)
        self.pushButtonShowEmail = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonShowEmail.setGeometry(QtCore.QRect(300, 580, 300, 100))
        self.pushButtonShowEmail.clicked.connect(self.showEmails)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonShowEmail.setFont(font)
        self.pushButtonShowEmail.setObjectName("pushButtonShowEmail")
        self.pushButtonFilterEmail = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonFilterEmail.setGeometry(QtCore.QRect(680, 580, 300, 100))
        self.pushButtonFilterEmail.clicked.connect(self.filterEmails)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButtonFilterEmail.setFont(font)
        self.pushButtonFilterEmail.setObjectName("pushButtonFilterEmail")
        
        TabWidget.addTab(self.tab_4, "")


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
        self.pushButton_4.clicked.connect(self.setAvatar)
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

        music_file_1 = QUrl.fromLocalFile(self.root + '\\media\\receive.mp3')
        content_1 = QtMultimedia.QMediaContent(music_file_1)
        self.player_1 = QtMultimedia.QMediaPlayer()
        self.player_1.setMedia(content_1)
        self.player_1.setVolume(30)

        music_file_2 = QUrl.fromLocalFile(self.root + '\\media\\record_start.mp3')
        content_2 = QtMultimedia.QMediaContent(music_file_2)
        self.player_2 = QtMultimedia.QMediaPlayer()
        self.player_2.setMedia(content_2)
        self.player_2.setVolume(30)

    def setAvatar(self):
        filename = QFileDialog.getOpenFileNames(
            self, 'Select an image', os.getcwd(), "Image Files(*.ico *.jpg *.png *.bmp)")
        print(filename)
        self.avatar = QPixmap(filename[0][0]).scaled(50, 50)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "CSC3180 Project Chat Bot"))
        self.pushButton.setText(_translate("TabWidget", "Send"))
        self.pushButton_speak.setText(_translate("TabWidget", "Speak"))

        TabWidget.setTabText(TabWidget.indexOf(self.tab),
                             _translate("TabWidget", "Chatting"))
        self.pushButton_2.setText(_translate("TabWidget", "Set Font"))

        self.pushButton_3.setText(_translate("TabWidget", "Set Font Size"))

        self.pushButton_4.setText(_translate("TabWidget", "Set Avatar"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2),
                             _translate("TabWidget", "Settings"))
        self.textBrowser.setHtml(_translate("TabWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> Developed by Mingzhuo Yang (118020068), Wei Wu (118010335), and Tao Pan (119010239) </p></body></html>"))
        self.label.setText(_translate("TabWidget", "About"))
        self.label_2.setText(_translate(
            "TabWidget", "CSC3180 Project - Chat Bot"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_3),
                             _translate("TabWidget", "Info"))
        
        TabWidget.setTabText(TabWidget.indexOf(self.tab_4),
                             _translate("TabWidget", "Emails"))
        self.pushButtonShowEmail.setText(_translate("TabWidget", "Show Emails"))
        self.pushButtonFilterEmail.setText(_translate("TabWidget", "Filter Emails"))

        # Set Font
    def setFontFamily(self):
        text = self.comboBox.currentText()
        fontDict = {'Arial': 'Arial', 'Courier New': 'Courier New',
                    'TimesNewRoman': 'TimesNewRoman'}
        font = QtGui.QFont()
        font.setFamily(fontDict[text])
        self.TabWidget.setFont(font)
        self.resetDialogsAndEmails()

    def setFontSize(self):
        text = self.comboBox_2.currentText()
        font = QtGui.QFont()
        font.setPointSize(int(text))
        self.TabWidget.setFont(font)
        self.resetDialogsAndEmails()

    def sendMessageUser(self, text):
        self.addDialog("User", text)
        # TODO: send the user input to AI

        # Use thread to call bot
        try:
            # If the thread is running (bot is processing the previous task)
            # Tell user that it is busy and ignore the new input
            if self.t.isRunning():
                # self.t.raise_exception()
                msg = 'I am still thinking about \'' + self.input_buffer + '\', please wait a minute.'
                self.sendMessageBot(msg)
            # If the bot is not busy, start a new task
            else:
                text = text.replace('\n', ' ').replace('\r', ' ')
                self.input_buffer = text
                #self.t.output.disconnect(self.sendMessageBot)
                self.t = uiThreadChatter(self, text)
                #self.t = uiThreadSearch(self, text)
                self.t.output.connect(self.sendMessageBot)
                self.t.start()
        # If self.t is not defined (the first task)
        # Start a new task
        except:
            text = text.replace('\n', ' ').replace('\r', ' ')
            self.input_buffer = text
            # self.t = uiThreadSearch(self, text)
            self.t = uiThreadChatter(self, text)
            self.t.output.connect(self.sendMessageBot)
            self.t.start()

    def sendMessageUserFromTextEdit(self):
        text = self.textEdit.toPlainText()
        if text != "":
            self.textEdit.clear()
            self.sendMessageUser(text)
        
    # TODO: AI sends output to here
    def sendMessageBot(self, text):
        self.player_1.play()
        self.addDialog("Bot", text)

    def addDialog(self, sender, text):
        chatBlock = QtWidgets.QLabel()
        chatBlock.setGeometry(QtCore.QRect(0, 0, 1240, 451))
        chatBlock.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        avatar = QtWidgets.QLabel(chatBlock)
        avatar.setGeometry(10, 10, 50, 50)
        avatar.setAlignment(QtCore.Qt.AlignCenter)
        avatar.setScaledContents(True)
        msgBox = QtWidgets.QTextBrowser(chatBlock)
        if sender == "User":
            msgBox.setAutoFillBackground(True)
            p = msgBox.viewport().palette()
            p.setColor(msgBox.viewport().backgroundRole(), QColor(149, 236, 105))
            msgBox.viewport().setPalette(p)
            avatar.setPixmap(self.avatar)
        else:
            avatar.setPixmap(self.avatarBot)
        msgBox.setGeometry(QtCore.QRect(70, 0, 1170, 451))
        msgBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        msgBox.setObjectName("msgBox"+str(self.dialog_id))
        #msgBox.document().setPlainText(str(text))
        msgBox.setText(str(text))
        self.verticalLayout.addWidget(chatBlock)
        self.msgBoxes.append(msgBox)
        # Force the UI to update so that msgBox.document().size().height() works correctly
        QtWidgets.qApp.processEvents()
        boxHeight = msgBox.document().size().height() * 1.05
        if boxHeight < 70:
            boxHeight = 70
        # print(boxHeight)
        msgBox.setMinimumHeight(boxHeight)
        msgBox.setMaximumHeight(boxHeight)
        chatBlock.setMinimumHeight(boxHeight)
        chatBlock.setMaximumHeight(boxHeight)

    def resetDialogsAndEmails(self):
        for msgBox in self.msgBoxes:
            boxHeight = msgBox.document().size().height() * 1.05
            if boxHeight < 70:
                boxHeight = 70
            # print(boxHeight)
            msgBox.setMinimumHeight(boxHeight)
            msgBox.setMaximumHeight(boxHeight)
            msgBox.parentWidget().setMinimumHeight(boxHeight)
            msgBox.parentWidget().setMaximumHeight(boxHeight)
        for emailBox in self.emailBoxes:
            boxHeight = emailBox.document().size().height() * 1.05
            if boxHeight < 70:
                boxHeight = 70
            # print(boxHeight)
            emailBox.setMinimumHeight(boxHeight)
            emailBox.setMaximumHeight(boxHeight)

    def scrollToBottomChatBox(self):
        scrollBar = self.scrollArea.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())

    def setTextEdit(self, text):
        self.textEdit.setText(text)

    # TODO: Voice recognition interface
    def startVoiceRecording(self):
        self.player_2.play()
        self.t = uiThreadSpeech(self)
        self.t.output.connect(self.setTextEdit)
        self.t.start()
        return

    # def endVoiceRecording(self):
    #     msg = ""
    #     return

    def addEmail(self, sender="", text="", label=""):
        emailBox = QtWidgets.QTextBrowser(self.tab_4)
        emailBox.setGeometry(QtCore.QRect(20, 0, 1200, 451))
        emailBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        emailBox.setObjectName("emailBox"+str(self.email_id))
        self.email_id += 1
        #msgBox.document().setPlainText(str(text))
        emailBox.setText(str(text))
        emailBox.setAutoFillBackground(True)
        if label != "":
            p = emailBox.viewport().palette()
            if label == "ham":
                p.setColor(emailBox.viewport().backgroundRole(), QColor(149, 236, 105))
            elif label == "spam":
                p.setColor(emailBox.viewport().backgroundRole(), QColor(255, 106, 106))
            emailBox.viewport().setPalette(p)
        self.verticalLayoutEmail.addWidget(emailBox)
        self.emailBoxes.append(emailBox)
        # Force the UI to update so that msgBox.document().size().height() works correctly
        QtWidgets.qApp.processEvents()
        boxHeight = emailBox.document().size().height() * 1.05
        if boxHeight < 70:
            boxHeight = 70
        # print(boxHeight)
        emailBox.setMinimumHeight(boxHeight)
        emailBox.setMaximumHeight(boxHeight)

    def setEmailLabel(self, emailBox, label):
        p = emailBox.viewport().palette()
        if label == "ham":
            p.setColor(emailBox.viewport().backgroundRole(), QColor(149, 236, 105))
        elif label == "spam":
            p.setColor(emailBox.viewport().backgroundRole(), QColor(255, 106, 106))
        emailBox.viewport().setPalette(p)

    def showEmails(self):
        
        item_list = list(range(self.verticalLayoutEmail.count()))
        item_list.reverse()

        for i in item_list:
            item = self.verticalLayoutEmail.itemAt(i)
            self.verticalLayoutEmail.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        
        QtWidgets.qApp.processEvents()
        
        self.emailBoxes.clear()

        count = 0
        with open(self.root+'//spam.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.addEmail(text=row[1])
                count += 1
                if count > self.max_n_emails:
                    break

        QtWidgets.qApp.processEvents()
        

    def filterEmails(self):
        for emailBox in self.emailBoxes:
            text = emailBox.document().toPlainText()
            # TODO: get the label
            import random
            label = random.randint(0,1)
            if label == 0:
                label = "ham"
            if label == 1:
                label = "spam"
            self.setEmailLabel(emailBox, label)

class uiThreadChatter(uiThread):
    def __init__(self, ui, text):
        uiThread.__init__(self)
        self.ui = ui
        self.ch = ui.ch
        self.text = text

    def run(self):
        if self.ch.user_info['user_info']['first_meet'] == 1:
            try:
                self.ch.user_info['user_info']['name'] = self.text
                self.output.emit("OK, {}, now you can ask me to do something or free talk with me.".format(self.text))
                self.ch.user_info['user_info']['first_meet'] = 0
                json.dump(self.ch.user_info, open(self.ui.root + '\\Chatter\\json\\user_info.json', 'w'))
            except:
                result = '''We are having trouble with the chatter, please try again later.'''
                self.output.emit(result)
        else:
            try:
                result = self.ch.UI2Chatter(self.text)
                self.output.emit(result)
            except:
                result = '''We are having trouble with the chatter, please try again later.'''
                self.output.emit(result)


class uiThreadSpeech(uiThread):
    def __init__(self, ui):
        uiThread.__init__(self)
        self.ui = ui

    def run(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.ui.r.listen(source)
            self.ui.player_2.play()
        try:
            text = self.ui.r.recognize_google(audio)
            self.output.emit(text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service" + format(e))


class Chatter:
    def __init__(self, ex):
        self.ui = ex
        # nltk word package
        nltk.data.path.append(self.ui.root + "\\nltk_data\\")
        self.model = load_model(self.ui.root + '\\Chatter\\model\\chatter_model.h5')
        self.knowledge = json.loads(open(self.ui.root + '\\Chatter\\json\\knowledge.json').read())
        self.words = pickle.load(open(self.ui.root + '\\Chatter\\pkl\\words.pkl', 'rb'))
        self.types = pickle.load(open(self.ui.root + '\\Chatter\\pkl\\types.pkl', 'rb'))
        self.WNL = WordNetLemmatizer()
        self.user_info = json.loads(open(self.ui.root + '\\Chatter\\json\\user_info.json').read())

        # check whether it is first meet
        if self.user_info['user_info']['first_meet'] == 1:
            self.Chatter2UI("Hello, nice to meet you! I am your chat bot.")
            self.Chatter2UI("As this is our first meeting, to provide a better assistance, I would like to ask your name.")
        else:
            self.Chatter2UI("Hello, I am here.")

    def run(self, input_text):
        self.UI2Chatter(self, input_text)

    def Chatter2UI(self, msg):
        self.ui.sendMessageBot(msg)

    def UI2Chatter(self, input_text):
        result = self.chatbot_response(input_text)
        return result

    def task_affair(self):
        return 0

    def task_email(self, msg):
        self.t = uiThreadEmailFilter(self, msg)
        self.t.output.connect(self.ui.sendMessageBot)
        self.t.start()
        return

    def task_search(self, msg):
        self.t = uiThreadSearch(self,  msg)
        self.t.output.connect(self.ui.sendMessageBot)
        self.t.start()
        return

    # match the words in sentence to bag
    def match_words(self, sentence, words):
        in_words = nltk.word_tokenize(sentence)
        in_words = [self.WNL.lemmatize(word.lower()) for word in in_words]
        bag = [0] * len(words)
        for s in in_words:
            flag = 0
            for i, w in enumerate(words):
                if s == w:
                    bag[i] = 1
                    flag = 1
            if not flag:
                i_max = 0
                bag_max = 0
                for i, w in enumerate(words):
                    l = [0 if a.path_similarity(b) is None else a.path_similarity(b) for a in wordnet.synsets(s) for b
                         in wordnet.synsets(w)]
                    if len(l) > 0:
                        bag_max = max(l) if max(l) > bag_max else bag_max
                        i_max = i
                bag[i_max] = bag_max
        return np.array(bag)

    # match the types for the sentence by pretrained model
    def match_types(self, sentence, model):
        bag = self.match_words(sentence, self.words)
        res = model.predict(np.array([bag]))[0]
        results = [[i, r] for i, r in enumerate(res)]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for result in results:
            return_list.append({"type": self.types[result[0]], "probability": result[1]})
        return return_list

    # special task special operation
    def get_response(self, types, msg, knowledge_json):
        tag = types[0]['type']
        prob = types[0]['probability']
        list_knowledge = knowledge_json['knowledge']
        if tag == "task_affair":
            response = "do task_affair" + "\t---confidence {}".format(prob)
            self.task_affair()
        elif tag == "task_email":
            response = "do task_email" + "\t---confidence {}".format(prob)
            self.task_email()
        elif tag == "task_search" or prob < 0.5:
            response = "I will google " + "\"" + msg + "\" " + " for you, please wait.\t---confidence {}".format(prob)
            self.task_search(msg)
        else:
            for k in list_knowledge:
                if k['tag'] == tag:
                    if tag == "greeting":
                        response = random.choice(k['out']).format(
                            self.user_info['user_info']['name']) + "\t---confidence {}".format(prob)
                    elif tag == "ask_user_info":
                        response = random.choice(k['out']).format(
                            self.user_info['user_info']['name']) + "\t---confidence {}".format(prob)
                    else:
                        response = random.choice(k['out']) + "\t---confidence {}".format(prob)
                    break
        return response

    # return the response
    def chatbot_response(self, msg):
        ints = self.match_types(msg, self.model)
        res = self.get_response(ints, msg, self.knowledge)
        return res


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ui_TabWidget()
    ex.show()
    ex.setFontSize()
    app.exec_()
