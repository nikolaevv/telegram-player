from telethon import TelegramClient, sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest
from config import api_id, api_hash, phone, chat_url
import os
import sqlite3
import time

session_name = 'Name_of_session'
# Название для сессии
work_dir = os.path.dirname(os.path.abspath(__file__))
# Абсолютный путь к директории файла

client = TelegramClient(session_name, api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    #client.send_code_request(phone)
    # Необходимо включить при первом использовании
    client.sign_in(phone, input('Enter code: '))

client.start()

def get_all_messages(channel):
    offset_msg = 140
    limit_msg = 0
    # Отступ от начала и максимальное число сообщений

    total_messages = 0
    total_count_limit = 0

    history = client(GetHistoryRequest(
		peer = channel,
		offset_id = offset_msg,
		offset_date = None, add_offset = 0,
		limit = limit_msg, max_id = 0, min_id = 0,
		hash = 0
    ))

    if not history.messages:
        # При пустом чате
        return False

    messages = history.messages
    messages.reverse()
    print(len(messages))

    for msg in messages:
        if msg.audio != None:
            with sqlite3.connect(f'{work_dir}/music.db') as connect:
                cursor = connect.cursor()
                sql = f'''
                    SELECT title
                    FROM music
                '''

                cursor.execute(sql)
                current_music = cursor.fetchall()

            title = msg.audio.attributes[0].title.replace('?', '')
            print(title)
            performer = msg.audio.attributes[0].performer
            duration = msg.audio.attributes[0].duration
            # Получение исполнителя, названия трека и его длительности

            if (title, ) not in current_music:
                downloaded_audio = os.listdir(path = f'{work_dir}/audio')
                if title not in downloaded_audio:
                    client.download_media(message = msg, file = f'audio/{title}.mp3')
                    # Скачивание аудиозаписи

                with sqlite3.connect(f'{work_dir}/music.db') as connect:
                    cursor = connect.cursor()
                    sql = '''INSERT INTO music
                             (title, performer, duration) VALUES (?, ?, ?)
                          '''
                    # Запись трека в базу данных

                    cursor.execute(sql, (title, performer, duration))
                    connect.commit()
                print(title)
                time.sleep(5)

channel = client.get_entity(chat_url)
# Получение объекта канала по его ссылке
messages = get_all_messages(channel)
# Скачивание новых аудио и занесение их в БД
