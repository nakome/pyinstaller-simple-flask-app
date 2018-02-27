from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template


import os
import json
import sys
import time
import shutil
import datetime

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


app.jinja_env.filters['datetime'] = formatDate


from app.controllers.notes import Notes
from app.controllers.media import Media


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
    # get all notes
    notes = Notes.get_all(work_path,offset)
    return render_template('index.html',data=notes,config=config)

@app.route('/notes/get/<int:uid>')
def note(uid):
    # get all notes
    notes = Notes.get_all(work_path,1)
    note = Notes.get_one(work_path,uid)
    return render_template('preview.html',data=notes,note=note,config=config)



"""
    Edit,add and delete note
"""
@app.route('/notes/edit/<int:uid>')
def edit(uid):
    # get all notes
    notes = Notes.get_all(work_path,1)
    note = Notes.get_one(work_path,uid)
    return render_template('edit.html',data=notes,note=note,config=config)
@app.route('/notes/new')
def new():
    # get all notes
    notes = Notes.get_all(work_path,1)
    return render_template('new.html',data=notes,config=config)

@app.route('/notes/delete/<int:uid>')
def delete(uid):
    return 'dalete note',uid















'''
    Login page
'''
@app.route('/login', methods=['GET', 'POST'])
def login():

    # use config vats
    username = config.username
    password = config.password

    msg = ''
    if request.method == 'POST':
        if request.form['username'] == username and request.form['password'] == password:
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for('index'))
        else :
            return redirect(url_for('login'))
    return render_template('views/login.html',msg=msg)



'''
    Logout page
'''
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)





