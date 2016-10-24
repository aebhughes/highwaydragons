#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 AEB Hughes
# All Rights Reserved.
# 110-111-767

from flask import (Flask, 
                   render_template,
                   request,
                   session,
                   url_for, 
                   redirect, 
                   g,
                   flash)
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object('settings')

from werkzeug.utils import secure_filename

from datetime import datetime, date

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/contact-us')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
