from flask import Flask
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import Markup

from flaskext.markdown import Markdown

import os
import json
import sys
import time
import shutil
import datetime
from math import ceil
import sqlite3

import jinja2_highlight



'''
    Get all files of folder
'''
def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

'''
    Format date
'''
def formatDate(t):
    return datetime.datetime.fromtimestamp(int(t)).strftime('%d-%m-%Y')


"""
    Copy files os static data
"""
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


class MyFlask(Flask):
    jinja_options = dict(Flask.jinja_options)
    jinja_options.setdefault('extensions',[]).append('jinja2_highlight.HighlightExtension')



"""
    The name of app check makeApp.spec
"""
appName = 'MyApp'


# init app
app = MyFlask(__name__)

app.secret_key = 'b2bc79f021f33610d6211f259f3ee09664bc5a0d971a183a'

Markdown(app)

app.jinja_env.filters['datetime'] = formatDate




class Notes:

    def update_note(path,uid):
        try:
            title = request.form.get('title')
            desc = request.form.get('description')
            category = request.form.get('category')
            content = request.form.get('content')
            favorite = request.form.get('favorite')

            with sqlite3.connect(path+'/storage.sqlite') as db:
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
                flash('Success the note has been updated !')
        except:
            db.rollback()
            flash('Error failed on update note! ')
        finally:
            db.close()
            return redirect('/notes/get/'+str(uid))


    def save_note(path):
        try:
            title = request.form.get('title')
            desc = request.form.get('description')
            category = request.form.get('category')
            content = request.form.get('content')
            isfavorite = request.form.get('favorite')

            with sqlite3.connect(path+'/storage.sqlite') as db:
                cur = db.cursor()
                sql = """INSERT INTO notes
                    (title,desc,category,content,isfavorite)
                    VALUES (?,?,?,?,?)"""

                cur.execute(sql,(title,desc,category,content,isfavorite))
                db.commit()
                flash('Success the note has been added')
        except:
            db.rollback()
            flash('Error in insert operation')
        finally:
            db.close()
            return redirect('/')


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
        db.close()
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
        db.close()
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
        db.close()
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


    '''
        Delete snippet
    '''
    def delete(path,uid):
        t = (uid,)
        try:
            with sqlite3.connect(path+'/storage.sqlite') as db:
                cur = db.cursor()
                cur.execute("DELETE FROM notes WHERE uid=?",t)
                db.commit()
                flash('Success the note has been deleted!')
        except:
            db.rollback()
            flash('Error in delete operation')
        finally:
            db.close()
            return redirect('/')




"""
    Define temp and dir path
"""
tmp_path = app.root_path
dir_path = sys.executable.replace(appName,'')


"""
    If DEBUG false use static data dir
    if not use data folder of executable file
    remember set False on compile
    python3 -m PyInstaller -F makeApp.spec
"""
DEBUG = True
config = ''
work_path = ''
if DEBUG:
    work_path = tmp_path+'/static/data'
    config_file = open(tmp_path+'/static/data/config.json','r')
    config = json.loads(config_file.read())
    pass
else:
    work_path = dir_path+'/data'
    if os.path.isdir(work_path) == False:
        os.mkdir(dir_path+'/data')
        copytree(tmp_path+'/static/data',dir_path+'/data')
    config_file = open(dir_path+'data/config.json','r')
    config = json.loads(config_file.read())







"""
    Show Dashboard and notes
"""
@app.route('/')
@app.route('/index')
def init(offset = 1):
    return render_template('index.html',config=config)

@app.route('/settings')
def settings():
    return render_template('settings.html',config=config)

@app.route('/notes/get/<int:uid>')
def note(uid):
    note = Notes.get_one(work_path,uid)
    return render_template('preview.html',note=note,config=config)



"""
    Ajax functions
"""
@app.route('/notes/get/all',methods=['GET'])
def all_notes():
    # get all notes
    notes = Notes.get_all(work_path,1)
    return notes

@app.route('/notes/search/<name>',methods=['GET'])
def search_notes(name):
    # get all notes
    notes = Notes.search(work_path,name,1)
    return notes





"""
    Edit,add and delete note
"""
@app.route('/notes/edit/<int:uid>',methods=['GET','POST'])
def edit(uid):

    if request.method == 'POST':
        return Notes.update_note(work_path,uid);

    note = Notes.get_one(work_path,uid)
    return render_template('edit.html',note=note,config=config)

@app.route('/notes/new', methods=['GET', 'POST'])
def new():

    if request.method == 'POST':
        return Notes.save_note(work_path);

    return render_template('new.html',config=config)


@app.route('/notes/delete/<int:uid>')
def delete(uid):
    return Notes.delete(work_path,uid);



@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)





