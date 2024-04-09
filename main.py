from flask import Flask, render_template, jsonify
import sqlite3


app = Flask(__name__)


# Function to retrieve information from the database
def get_information_from_database():
   conn = sqlite3.connect('your_database.db')  # Replace 'your_database.db' with your database file
   cursor = conn.cursor()
   cursor.execute('SELECT * FROM your_table')  # Replace 'your_table' with your table name
   rows = cursor.fetchall()
   conn.close()
   return rows


@app.route('/get_information', methods=['GET'])
def get_information():
   information = get_information_from_database()
   return jsonify(information)


if __name__ == '__main__':
   app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, g
from dynaconf import Dynaconf
from datetime import date
from datetime import datetime


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
   return pymysql.connect (
       database = 'sports_aggregator',
       user = 'lfrancois',
       password = '231566837',
       host = '10.100.33.60',
       cursorclass=pymysql.cursors.DictCursor,
       autocommit=True)

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
   return render_template('feed.html.jinja')


@app.route('/feed')
def post_feed():
   cursor = get_db().cursor()
   cursor.execute("""
   SELECT * FROM `Games`
   INNER JOIN `Teams` t1 ON `Games`.Team1 = t1.`ID`
   INNER JOIN `Teams` t2 ON `Games`.Team2 = t2.`ID`;
   """)
   results = cursor.fetchall()
   cursor.execute(""" SELECT * FROM `Sites` """)
   results2 = cursor.fetchall()
   cursor.close()
   return render_template("feed.html.jinja",Games=results,Sites=results2)


def index():
   cursor = get_db().cursor()
   cursor.execute('SELECT * from `Videos` ORDER BY `Timestamp`')
   results = cursor.fetchall()
   cursor.close()
   return render_template()


def noti():
   cursor = get_db().cursor()
   cursor.execute("SELECT datetime('now', 'localtime')")
   current_datetime = cursor.fetchone()[0]
   print("Current Date and Time from the database:", current_datetime)


