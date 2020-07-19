import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtGui import QIcon
from player import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.Qt import QLabel, pyqtSignal
from PyQt5.QtMultimedia import *


import telebot
import requests
from config import token
import sqlite3
import os

'''
TODO:
- задать текст последней аудио при запуске
'''

work_dir = os.path.dirname(os.path.abspath(__file__))

class SongList(QtWidgets.QMainWindow):
    def __init__(self):
        super(SongList, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.button_play_start)
        self.is_playlist_formed = False
        self.songs = []
        self.init_UI()
        self.player = QtMultimedia.QMediaPlayer()
        #self.ui.pushButton.clicked.connect(lambda: print(1))

    def button_play_start(self):
        print(self.player)
        if self.is_playlist_formed == True:
            self.player.play()
        else:
            self.play(0)
            self.is_playlist_formed = True

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_2.setIcon(icon)
        self.ui.pushButton_2.clicked.disconnect()
        self.ui.pushButton_2.clicked.connect(self.button_play_stop)

    def button_play_stop(self):
        self.player.pause()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_2.setIcon(icon)

        self.ui.pushButton_2.clicked.disconnect()
        self.ui.pushButton_2.clicked.connect(self.button_play_start)

    def init_UI(self):
        self.setWindowTitle('Музыка из Telegram')
        self.setWindowIcon(QIcon(f'{work_dir}/logo.png'))

    def play(self, id):
        self.player = QtMultimedia.QMediaPlayer()
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        # Создание плеера и плейлиста для него

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_2.setIcon(icon)

        self.ui.pushButton_2.clicked.disconnect()
        self.ui.pushButton_2.clicked.connect(self.button_play_stop)
        # Назначение команд для кнопки

        for media in range(id, len(self.songs)):
            title, performer = self.songs[media][0], self.songs[media][1]
            print(title)
            downloaded_audio = os.listdir(path = f'{work_dir}/audio')
            print(downloaded_audio)
            # Получение списка скачанных аудио

            if media == id:
                self.ui.performer.setText(performer)
                self.ui.main_title.setText(title)

            print(f'{work_dir}/audio/{title}.mp3')
            print(id)
            self.url = QtCore.QUrl.fromLocalFile(f'{work_dir}/audio/{title}.mp3')
            self.content = QtMultimedia.QMediaContent(self.url)
            self.playlist.addMedia(self.content)

        self.player.play()

    def add_song(self, title, performer, duration, id):
        self.ui.song = QtWidgets.QWidget(self.ui.verticalLayoutWidget)
        self.ui.song.setEnabled(True)
        self.ui.song.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ui.song.setObjectName("song")
        self.ui.song.setMinimumSize(QtCore.QSize(100, 45))
        # Инициализация контейнера для композиции

        self.songs.append([title, performer])

        if len(title) > 17:
            title = title[:17] + '...'
        if len(performer) > 17:
            performer = performer[:17] + '...'
        # Сокращение имени автора или названия при большом кол-во символов

        self.ui.title = QtWidgets.QLabel(self.ui.song)
        self.ui.title.setGeometry(QtCore.QRect(60, 0, 130, 21))
        font = QtGui.QFont()
        font.setFamily("SF UI Text")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.ui.title.setFont(font)
        self.ui.title.setStyleSheet("color: #FFF;")
        self.ui.title.setObjectName("title")
        # Инициализация названия

        self.ui.author = QtWidgets.QLabel(self.ui.song)
        self.ui.author.setGeometry(QtCore.QRect(60, 20, 170, 21))
        font = QtGui.QFont()
        font.setFamily("SF UI Display")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ui.author.setFont(font)
        self.ui.author.setStyleSheet("color: #7c7c7e;")
        self.ui.author.setObjectName("author")
        # Инициализация автора

        self.ui.cover = QtWidgets.QLabel(self.ui.song)
        self.ui.cover.setEnabled(True)
        self.ui.cover.setGeometry(QtCore.QRect(10, 0, 41, 41))
        self.ui.cover.setMaximumSize(QtCore.QSize(41, 41))
        self.ui.cover.setSizeIncrement(QtCore.QSize(0, 0))
        self.ui.cover.setBaseSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ui.cover.setFont(font)
        self.ui.cover.setStyleSheet("border-radius: 50%;")
        self.ui.cover.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ui.cover.setText("")
        self.ui.cover.setPixmap(QtGui.QPixmap("cover.png"))
        self.ui.cover.setScaledContents(True)
        self.ui.cover.setObjectName("cover")
        # Инициализация обложки и назначение картинки к ней

        self.ui.duration = QtWidgets.QLabel(self.ui.song)
        self.ui.duration.setGeometry(QtCore.QRect(280, 10, 31, 16))
        font = QtGui.QFont()
        font.setFamily("SF UI Display")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ui.duration.setFont(font)
        self.ui.duration.setStyleSheet("color: #7c7c7e;")
        self.ui.duration.setObjectName("duration")
        # Инициализация длительности композиции

        self.ui.pushButton = QtWidgets.QPushButton(self.ui.song)
        self.ui.pushButton.setGeometry(QtCore.QRect(-2, 0, 341, 51))
        self.ui.pushButton.setText("")
        self.ui.pushButton.setDefault(False)
        self.ui.pushButton.setFlat(True)
        self.ui.pushButton.setObjectName("pushButton")
        self.ui.pushButton.setStyleSheet("opacity: 0;")
        self.ui.pushButton.clicked.connect(lambda: self.play(id))
        # Кнопка для отслеживания кликов по аудиозаписи

        #self.ui.verticalLayout.addWidget(self.ui.song)

        self.ui.title.setText(title)
        self.ui.author.setText(performer)
        self.ui.duration.setText(duration)
        # Задание тектовых значений

        self.ui.verticalLayout.addWidget(self.ui.song)
        # Добавление в главный контейнер


app = QtWidgets.QApplication([])
application = SongList()
application.setFixedSize(320, 475)
# Задание фиксированных сторон

with sqlite3.connect(f'{work_dir}/music.db') as connect:
    cursor = connect.cursor()
    sql = f'''
        SELECT title, performer, duration
        FROM music
    '''

    cursor.execute(sql)
    audios = cursor.fetchall()
    audios.reverse()

#audios = [{'duration': 214, 'title': 'Invisible', 'performer': 'Linkin Park', 'file_id':'CQACAgIAAx0CVaejCAACAh9fCvs4bViXwB0ufVIxIkyXKBH5YAAC0QIAAhacuUjsmipaGSKoFxoE'},
#{'duration': 298, 'title': 'Chlorine', 'performer': 'Twenty One Pilots', 'file_id':'CQACAgIAAx0CVaejCAACAh9fCvs4bViXwB0ufVIxIkyXKBH5YAAC0QIAAhacuUjsmipaGSKoFxoE'}]

for audio in audios:
    minutes = int(audio[2] % 60)
    duration = f'{audio[2] // 60}:{minutes // 10}{minutes % 10}'
    # Форматирование длительности аудио
    application.add_song(audio[0], audio[1], duration, audios.index(audio))
    # Добавление песни
    if audios.index(audio) == 0:
        application.ui.performer.setText(audio[1])
        application.ui.main_title.setText(audio[0])

print(application.songs)
application.show()

sys.exit(app.exec())
