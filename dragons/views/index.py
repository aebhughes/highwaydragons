from flask import Blueprint, render_template
from dragons import models

mod = Blueprint('index',__name__)

@mod.route('/')
def index():
    m = models.Member()
    m.print_club()
    return render_template('index.html')

@mod.route('/members')
def members():
    return render_template('members.html')

@mod.route('/contact-us')
def contact():
    return render_template('contact.html')

