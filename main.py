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
        self.song = QtWidgets.QWidget()
        self.song.setEnabled(True)
        self.song.setMaximumSize(QtCore.QSize(16777215, 80))
        self.song.setObjectName("song")

        self.title = QtWidgets.QLabel(self.song)
        self.title.setGeometry(QtCore.QRect(100, 10, 41, 31))
        self.title.setStyleSheet("color: #FFF;")
        self.title.setObjectName("title")

        self.author = QtWidgets.QLabel(self.song)
        self.author.setGeometry(QtCore.QRect(100, 40, 91, 16))
        self.author.setStyleSheet("color: #FFF;")
        self.author.setObjectName("author")

        self.cover = QtWidgets.QLabel(self.song)
        self.cover.setEnabled(True)
        self.cover.setGeometry(QtCore.QRect(10, 10, 61, 61))
        self.cover.setMaximumSize(QtCore.QSize(5000, 6000))
        self.cover.setSizeIncrement(QtCore.QSize(0, 0))
        self.cover.setBaseSize(QtCore.QSize(100, 100))
        self.cover.setStyleSheet("border-radius: 30px;")
        self.cover.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.cover.setText("")
        self.cover.setPixmap(QtGui.QPixmap("../Trench_cover.jpg"))
        self.cover.setScaledContents(True)
        self.cover.setObjectName("cover")

        self.duration = QtWidgets.QLabel(self.song)
        self.duration.setGeometry(QtCore.QRect(210, 30, 31, 16))
        self.duration.setStyleSheet("color: #FFF;")
        self.duration.setObjectName("duration")

        self.gridLayout.addWidget(self.song, 0, 0, 1, 1)


app = QtWidgets.QApplication([])
application = SongList()

audios = [{'duration': 214, 'title': 'Invisible', 'performer': 'Linkin Park', 'file_id':'CQACAgIAAx0CVaejCAACAh9fCvs4bViXwB0ufVIxIkyXKBH5YAAC0QIAAhacuUjsmipaGSKoFxoE'}]

for audio in audios:
    #application.add_song(1, 1, 1)

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
application.add_song(1, 1, 1)

sys.exit(app.exec())
