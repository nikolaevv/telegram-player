import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from player import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget


import telebot
import requests
from config import token
import os

#response = requests.get(f'https://api.telegram.org/bot{token}/getUpdates', params = {'limit': 1000, 'offset': -1})
#print(response.text)

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

    def add_song(self, title, performer, duration):
        self.ui.song = QtWidgets.QWidget(self.ui.gridLayoutWidget)
        self.ui.song.setEnabled(True)
        self.ui.song.setMaximumSize(QtCore.QSize(16777215, 80))
        self.ui.song.setObjectName("song")

        self.ui.title = QtWidgets.QLabel(self.ui.song)
        self.ui.title.setGeometry(QtCore.QRect(100, 10, 41, 31))
        self.ui.title.setStyleSheet("color: #FFF;")
        self.ui.title.setObjectName("title")

        self.ui.author = QtWidgets.QLabel(self.ui.song)
        self.ui.author.setGeometry(QtCore.QRect(100, 40, 91, 16))
        self.ui.author.setStyleSheet("color: #FFF;")
        self.ui.author.setObjectName("author")

        self.ui.cover = QtWidgets.QLabel(self.ui.song)
        self.ui.cover.setEnabled(True)
        self.ui.cover.setGeometry(QtCore.QRect(10, 10, 61, 61))
        self.ui.cover.setMaximumSize(QtCore.QSize(5000, 6000))
        self.ui.cover.setSizeIncrement(QtCore.QSize(0, 0))
        self.ui.cover.setBaseSize(QtCore.QSize(100, 100))
        self.ui.cover.setStyleSheet("border-radius: 30px;")
        self.ui.cover.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ui.cover.setText("")
        self.ui.cover.setPixmap(QtGui.QPixmap("../Trench_cover.jpg"))
        self.ui.cover.setScaledContents(True)
        self.ui.cover.setObjectName("cover")

        self.ui.duration = QtWidgets.QLabel(self.ui.song)
        self.ui.duration.setGeometry(QtCore.QRect(210, 30, 31, 16))
        self.ui.duration.setStyleSheet("color: #FFF;")
        self.ui.duration.setObjectName("duration")

        self.ui.title.setText("Chlorine")
        self.ui.author.setText("twenty one pilots")
        self.ui.duration.setText("2:07")

        self.ui.gridLayout.addWidget(self.ui.song)


app = QtWidgets.QApplication([])
application = SongList()

audios = [{'duration': 214, 'title': 'Invisible', 'performer': 'Linkin Park', 'file_id':'CQACAgIAAx0CVaejCAACAh9fCvs4bViXwB0ufVIxIkyXKBH5YAAC0QIAAhacuUjsmipaGSKoFxoE'}]

for audio in audios:
    application.add_song(1, 1, 1)

    response = requests.get(f'https://api.telegram.org/bot{token}/getFile', params = {'file_id': audio['file_id']}).json()
    path = response['result']['file_path']

    u = open(f'{work_dir}/audio/{audio["title"]}.mp3', 'wb')
    # Открываем подкаст для записи, в режиме wb
    file = requests.get(f'https://api.telegram.org/file/bot{token}/{path}')
    # Делаем запрос

    """
    u.write(file.content)
    # Записываем содержимое в файл
    u.close()
    """

application.show()

sys.exit(app.exec())
