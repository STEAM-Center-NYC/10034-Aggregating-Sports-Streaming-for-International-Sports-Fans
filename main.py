from flask import Flask, render_template, request, redirect, url_for, g
from dynaconf import Dynaconf

import pymysql
import pymysql.cursors
from pprint import pprint as print 
import flask_login

app = Flask(__name__)

settings= Dynaconf(
    settings_file=('settings.toml')
)

class user:
    is_authenticated = True 
    is_anonymous = False
    is_active = True
    def __init__(self, id, username):
        self.username = username 
        self.id = id 
    def get_id(self):
        return str(self.id)


def connect_db():
    return pymysql.connect(
        database = 'sports_aggregator',
        user = settings.db_user,
        password = settings.db_pass,
        host = '10.100.33.60',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

@app.route('/')
def index():
        return render_template('landing.html.jinja')



@app.route('/feed')
def feed():
    cursor = get_db().cursor()
    cursor.close()
    return render_template('stream.html.jinja')