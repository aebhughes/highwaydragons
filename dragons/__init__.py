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

from dragons.views import index

app.register_blueprint(index.mod)
