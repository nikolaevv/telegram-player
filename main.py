import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from player import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.Qt import QLabel, pyqtSignal


import telebot
import requests
from config import token
import os

work_dir = os.path.dirname(os.path.abspath(__file__))

class SongList(QtWidgets.QMainWindow):
    def __init__(self):
        super(SongList, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Музыка из Telegram')
        self.setWindowIcon(QIcon(f'{work_dir}/logo.png'))

    def play(self):
        pass

    def add_song(self, title, performer, duration):
        self.ui.song = QtWidgets.QWidget(self.ui.gridLayoutWidget)
        self.ui.song.setEnabled(True)
        self.ui.song.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ui.song.setObjectName("song")
        # Инициализация контейнера для композиции

        self.ui.title = QtWidgets.QLabel(self.ui.song)
        self.ui.title.setGeometry(QtCore.QRect(60, 0, 71, 21))
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
        self.ui.author.setGeometry(QtCore.QRect(60, 20, 111, 21))
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
        self.ui.cover.setPixmap(QtGui.QPixmap("../Trench_cover.jpg"))
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
        self.ui.pushButton.clicked.connect(self.play)
        # Кнопка для отслеживания кликов по аудиозаписи

        self.ui.gridLayout.addWidget(self.ui.song)

        self.ui.title.setText(title)
        self.ui.author.setText(performer)
        self.ui.duration.setText(duration)
        # Задание тектовых значений

        self.ui.gridLayout.addWidget(self.ui.song)
        # Добавление в главный контейнер


app = QtWidgets.QApplication([])
application = SongList()
application.setFixedSize(320, 550)
# Задание фиксированных сторон

audios = [{'duration': 214, 'title': 'Invisible', 'performer': 'Linkin Park', 'file_id':'CQACAgIAAx0CVaejCAACAh9fCvs4bViXwB0ufVIxIkyXKBH5YAAC0QIAAhacuUjsmipaGSKoFxoE'}]

for audio in audios:
    response = requests.get(f'https://api.telegram.org/bot{token}/getFile', params = {'file_id': audio['file_id']}).json()
    path = response['result']['file_path']
    # Запрос на получение прямой ссылки на композицию

    u = open(f'{work_dir}/audio/{audio["title"]}.mp3', 'wb')
    #
    file = requests.get(f'https://api.telegram.org/file/bot{token}/{path}')
    # Запрос на получение файла

    """
    u.write(file.content)
    # Записываем содержимое в файл
    u.close()
    """
    minutes = int(audio['duration'] % 60)
    duration = f'{audio["duration"] // 60}:{minutes // 10}{minutes % 10}'
    # Форматирование длительности аудио
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    application.add_song(audio['title'], audio['performer'], duration)
    # Добавление песни на экран приложения

application.show()

sys.exit(app.exec())
