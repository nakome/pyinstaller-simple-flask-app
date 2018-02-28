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
import json

class Notes:
    
    def update_note(path,uid):
        title = request.form.get('title')
        desc = request.form.get('description')
        category = request.form.get('category')
        content = request.form.get('content')
        favorite = request.form.get('favorite')
        
        db = sqlite3.connect(path+'/storage.sqlite')
        cur = db.cursor()
        sql = """UPDATE notes
                SET title = ?,
                    desc = ?,
                    category = ?,
                    content = ?,
                    isfavorite = ?
                WHERE uid = ?"""
        cur.execute(sql,(title,desc,category,content,favorite,uid))
        db.commit()
        db.close()
        return redirect('/notes/get/'+str(uid))
        
    
    def get_all(path,offset):
        per_page = 16
        db = sqlite3.connect(path+'/storage.sqlite')
        db.row_factory = sqlite3.Row # para poder usar dot notacion
        cur = db.cursor()
        cur.execute('SELECT count(*) FROM notes')
        total = cur.fetchone()[0]
        total_pages = int(ceil(total / float(per_page)))
        sql = 'SELECT uid,title,desc,category FROM notes ORDER BY date LIMIT {}, {}'
        limit = int(ceil((float(per_page) * offset)) - float(per_page))
        cur.execute(sql.format(limit, per_page))
        rows = cur.fetchall()
        cur.close()
        data = []
        for item in rows:
            data.append({
                'uid': item[0],
                'title': item[1],
                'desc': item[2],
                'category':item[3]
            })
        return json.dumps(data)

    def search(path,name,offset):
        per_page = 16
        db = sqlite3.connect(path+'/storage.sqlite')
        db.row_factory = sqlite3.Row # para poder usar dot notacion
        cur = db.cursor()
        cur.execute('SELECT count(*) FROM notes')
        total = cur.fetchone()[0]
        total_pages = int(ceil(total / float(per_page)))
        sql = "SELECT uid,title,desc,category FROM notes WHERE title LIKE '%{}%' ORDER BY date LIMIT {}, {}"
        limit = int(ceil((float(per_page) * offset)) - float(per_page))
        cur.execute(sql.format(name,limit, per_page))
        rows = cur.fetchall()
        cur.close()
        data = []
        for item in rows:
            data.append({
                'uid': item[0],
                'title': item[1],
                'desc': item[2],
                'category':item[3]
            })
        return json.dumps(data)
    
    def get_one(path,uid):
        uid = (uid,)
        db = sqlite3.connect(path+'/storage.sqlite')
        cur = db.cursor()
        cur.execute('SELECT * FROM notes WHERE uid=?',uid)
        item = cur.fetchone()
        cur.close()
        data = {
            'uid': item[0],
            'title': item[1],
            'description': item[2],
            'date': item[3],
            'category': item[4],
            'content': Markup(item[5]),
            'favorite': item[6]
        }
        return data
