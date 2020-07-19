import sqlite3
import time
import os

work_dir = os.path.dirname(os.path.abspath(__file__))

with sqlite3.connect(f'{work_dir}/music.db') as connect:
    cursor = connect.cursor()
    sql = f'''
        CREATE TABLE "music" (
    	"title"	TEXT,
    	"performer"	TEXT,
        "duration" INT
        );
    '''

    cursor.execute(sql)
    connect.commit()
