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

@app.route('/admin/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        store = Store(user=request.form.get('username'))
        if store.doc:
            if store.doc['password'] == request.form.get('password'):
                session['academy'] = [store.key,
                                      datetime.strftime(date.today(), '%Y%m%d')]
                return redirect('/')
            flash('Password not recognised')
        else:
            flash('Username not recognised')
    return render_template('signin.html')

@app.route('/admin/logout', methods=['GET','POST'])
def logout():
    if 'hwdragons' in session:
        del session['hwdragons']
    return redirect('/admin/login')

@app.route('/admin', methods=['GET','POST'])
def admin():
    ref_id, last_date = session.get('hwdragons',(None,None))
    if not ref_id or last_date != str(date.taday()):
        del session['hwdragons']
        return redirect(url_for('login'))
    if request.method == 'POST':
        for fname in ('templates','static'):
            file = request.files[fname]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(fname, filename))
            
    

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
