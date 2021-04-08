import sqlite3
import json
import logging


class EventApi:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY autoincrement,
            data TEXT NOT NULL
        )""")
        try:
            self.conn.commit()
        except Exception as e:
            logging.exception(e)
            self.conn.rollback()
            raise e

    def add_event(self, data):
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO events (data) VALUES (?)""", (json.dumps(data), ))
        try:
            self.conn.commit()
            data.setdefault('id', cur.lastrowid)
            return data
        except Exception as e:
            self.conn.rollback()
            raise e

    def get_events(self):
        rs = {'events': []}
        cur = self.conn.cursor()
        for row in cur.execute('SELECT id, data FROM events'):
            id, data = row[0], json.loads(row[1])
            data['id'] = id
            rs['events'].append(data)

        return rs
