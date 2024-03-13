from flask import Flask, render_template, request, redirect, url_for, g
import pymysql
import pymysql.cursors
from pprint import pprint as print 
import flask_login

app = Flask(__name__)

class user:
    is_authenticated = True 
    is_anonymous = False
    is_active = True
    def __init__(self, id, username):
        self.id = id 
        self.username = username 
    def get_id(self):
        return str(self.id)


def connect_db():
    return pymysql.connect(
        database = 'lfrancois_Sports',
        user = 'lfrancois',
        password = '231566837',
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

def index():
    cursor = get_db().cursor()
    cursor.execute('SELECT * from `Videos` ORDER BY `Timestamp`')
    results = cursor.fetchall()
    cursor.close()
    return render_template()