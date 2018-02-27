from flask import Flask
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import Markup


from math import ceil
import os
import datetime
import time
import sqlite3

class Notes:

    def get_all(path,offset):
        per_page = 6
        db = sqlite3.connect(path+'/storage.db')
        db.row_factory = sqlite3.Row # para poder usar dot notacion
        cur = db.cursor()
        cur.execute('SELECT count(*) FROM notes')
        total = cur.fetchone()[0]
        total_pages = int(ceil(total / float(per_page)))
        sql = 'SELECT * FROM notes ORDER BY date LIMIT {}, {}'
        limit = int(ceil((float(per_page) * offset)) - float(per_page))
        cur.execute(sql.format(limit, per_page))
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_one(path,uid):
        uid = (uid,)
        db = sqlite3.connect(path+'/storage.db')
        cur = db.cursor()
        cur.execute('SELECT * FROM notes WHERE UID=?',uid)
        item = cur.fetchone()
        cur.close()
        data = {
            'uid': item[0],
            'title': item[1],
            'description': item[2],
            'content': Markup(item[3]),
            'category': item[4],
            'date': item[5],
            'update_at': item[6],
            'favorite': item[7]
        }
        return data
