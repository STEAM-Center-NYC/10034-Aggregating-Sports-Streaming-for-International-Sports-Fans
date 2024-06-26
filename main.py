from flask import Flask, render_template, request, redirect, url_for, g
from dynaconf import Dynaconf

import pymysql
import pymysql.cursors
from pprint import pprint as print 
import flask_login


app = Flask(__name__)
app.secret_key = "nugget_secret_recipe"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

settings= Dynaconf(
    settings_file=('settings.toml')
)

class User:
    is_authenticated = True 
    is_anonymous = False
    is_active = True
    def __init__(self, id, username):
        self.username = username 
        self.id = id 
    def get_id(self):
        return str(self.id)

@app.route('/signin',methods =['GET','POST'])
def Signin():
 if request.method == 'POST':
    Username = request.form["Username"]
    Password = request.form["Password"]
    cursor =get_db().cursor()
    cursor.execute(f"SELECT * FROM `User` WHERE `Username` = '{Username}'")   
    User = cursor.fetchone()
    {User['Password']}
    if Password == User["Password"]:
        user =load_user(User['ID'])
        flask_login.login_user(user)
        return redirect('/feed')
 return render_template("signin.html.jinja")

@app.route('/signup', methods=['GET', 'POST'])
def Signup():
 if request.method == 'POST':
    Username = request.form["Username"]
    Password = request.form["Password"]
    Name = request.form["Name"]
    User_Bio = request.form["User_Bio"]
    Email = request.form["Email"]
    cursor =get_db().cursor()
    cursor.execute(f"INSERT INTO `User` (`Username`,`Password`,`Name`,`User_Bio`,`Email`) VALUES ('{Username}','{Password}','{Name}','{User_Bio}','{Email}')")
    cursor.close()
    get_db().commit()
    return redirect("/signin")
 return render_template("signup.html.jinja")

def connect_db():
    return pymysql.connect(
        database="sports_aggregator",
        user ="sjamesjr",
        password="250415031",
        host = "10.100.33.60",
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
        INNER JOIN `Teams` t2 ON `Games`.Team2 = t2.`ID`
        LEFT JOIN `Leaugesite` ON t1.LeaugeID =  Leaugesite.LeaugeID
        LEFT JOIN `Sites` ON  Leaugesite.SiteID = Sites.ID
    """)
    results = cursor.fetchall()
    cursor.execute(""" SELECT * FROM `Sites` """)
    results2 = cursor.fetchall()
    cursor.execute(""" SELECT * FROM `League` """)
    results3=cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja",Games=results,Sites=results2,Leagues=results3)

@app.route('/FTeams/<int:Team_index>', methods=['POST'])
def todo_complete(Team_index):
    ID = flask_login.current_user.id
    cursor = get_db().cursor()
    cursor.execute(f"INSERT INTO `FTeams`(UserID,TeamID) VALUES ({ID},{Team_index});")
    cursor.close()
    get_db().cursor()
    return redirect('/')


@app.route('/FTeams')
def post_FvfszTeams():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `Teams`")
    results = cursor.fetchall()
    cursor.close()
    return render_template("favorite.html.jinja",Teams=results)

def index():
    cursor = get_db().cursor()
    results = cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja")

@app.route('/Profile')
@flask_login.login_required
def post_profile():
    ID = flask_login.current_user.id
    cursor = get_db().cursor()
    cursor.execute(f"""
    SELECT * FROM `User`  WHERE `ID` = '{ID}' """)
    results = cursor.fetchone()
    cursor.execute(f"SELECT * FROM `FTeams` INNER JOIN `Teams` ON `FTeams`.TeamID = Teams.`ID` WHERE `UserID` = {ID}")
    result2= cursor.fetchall()
    return render_template ("Profile.html.jinja",User=results,FTeams=result2)

@login_manager.user_loader
def load_user(user_id):
   cursor = get_db().cursor()
   cursor.execute(f"SELECT * FROM `User` WHERE `id` = {user_id}")
   result = cursor.fetchone()
   cursor.close()
   get_db().commit()
   if result is None:
    return None
   return User(result["ID"], result["Username"])

@app.route('/League/<int:League_index>')
def todo_delete(League_index):
    cursor = get_db().cursor()
    cursor.execute(f"""
    SELECT * FROM `Games` 
    INNER JOIN `Teams` t1 ON `Games`.Team1 = t1.`ID` 
    INNER JOIN `Teams` t2 ON `Games`.Team2 = t2.`ID`
    LEFT JOIN `Leaugesite` ON t1.LeaugeID =  Leaugesite.LeaugeID
    LEFT JOIN `Sites` ON  Leaugesite.SiteID = Sites.ID
    WHERE t1.`LeaugeID` = {League_index}
    """)
    results = cursor.fetchall()
    cursor.execute(""" SELECT * FROM `Sites` """)
    results2 = cursor.fetchall()
    cursor.execute(""" SELECT * FROM `League` """)
    results3=cursor.fetchall()
    cursor.execute(f""" SELECT * FROM `League` WHERE `ID` = {League_index}""")
    results4=cursor.fetchone()
    cursor.close()
    return render_template("blah.html.jinja",Games=results,Sites=results2,Leagues=results3,Leaguestuff=results4)
   