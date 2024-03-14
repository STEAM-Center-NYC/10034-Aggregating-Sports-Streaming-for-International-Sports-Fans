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
        database = 'lfrancois_Sports',
        user = 'settings.db_user',
        password = 'settings.db_pass',
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

@app.route('/feed')
def post_feed():
    cursor = get_db().cursor()
    cursor.execute("""
    SELECT * FROM `Games` 
    INNER JOIN `Teams` t1 ON `Games`.Team1 = t1.`ID` 
    INNER JOIN `Teams` t2 ON `Games`.Team2 = t2.`ID`; 
    """)
    results = cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja",Games=results)

def index():
    cursor = get_db().cursor()
    results = cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja")