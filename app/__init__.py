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


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)




app = Flask(__name__)



tmp_path = app.root_path
dir_path = sys.executable.replace('MyApp','')



'''
work_path = ''
if os.path.isdir(dir_path+'data'):
    work_path = dir_path+'data'
    pass
else:
    copytree(tmp_path+'/static/data',dir_path+'/static/data')
    work_path = dir_path+'data'
'''


@app.route('/')
@app.route('/index')
def init():
    data = {
        "tmp_path": tmp_path,
        "dir_path": dir_path,
    }
    return render_template('index.html',data=data)




@app.route('/test', methods=['POST'])
def test():

    app.logger.debug("JSON received...")
    app.logger.debug(request.json)

    if request.json:
        mydata = request.json
        return mydata.get('title')
    else:
        return "no json received"



@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)






