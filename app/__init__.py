from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template

import os
import json
import sys

app = Flask(__name__)

root = app.root_path

@app.route('/')
def init():
    data = {
        "root": root
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






