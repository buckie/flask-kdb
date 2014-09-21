from flask import Flask
from flask_kdb import KDB

app = Flask(__name__)
q = KDB(app)
app.config['SECRET_KEY'] = 'foobar'

from . import views


