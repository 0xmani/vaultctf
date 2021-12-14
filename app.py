from enum import unique
from os import name
from re import template
from flask import Flask, render_template, url_for, redirect, request, session
from flask.helpers import flash
from flask.templating import render_template_string
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import literal_column
from sqlalchemy.sql.functions import current_user, user
from datetime import datetime

msg = 'Invalid Username or Password.'
app = Flask(__name__)
app.config['SECRET_KEY'] = "S3cr3t"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True	
Session(app)

#database
db = SQLAlchemy(app)
class Users(db.Model):
   id = db.Column('uid', db.Integer, primary_key = True)
   user = db.Column(db.String(50), unique = True)
   passwd = db.Column(db.String(50))
   
   def __repr__(self):
        return 'user ' + str(self.user)

#routing
#routing to landing page

@app.route('/admin')
def admin():
    if session.get("name"):
        name1 = session["name"]       
        return render_template('admin.html', name=name1)
    else:
        return redirect('login')

@app.route('/')
def index():
    if session.get("name"):
        name1 = session["name"]       
        return render_template('index.html', name=name1)
    else:
        return render_template('index.html')

#flag is here

@app.route('/get_flag')
def getflag():
    return "VAULT{h4ppy_h4ck1ng}"

#login validation

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method =='GET':
        if session.get("name"):
            name1 = session["name"]
            return redirect('/')
        else:
            return render_template('login.html')
    else:
        pass
        if request.method == 'POST':
            u = request.form.get('user')
            p = request.form.get('pass')
            try:
                user_db = Users.query.filter_by(user=u).first().user
                pass_db = Users.query.filter_by(user=u).first().passwd
                if user_db == u and pass_db == p:
                    session['name'] = u
                    flash('Logged In as ' + u +'!')
                    return redirect('admin')
                else:
                    flash("Invalid Username or Password!")
                    return redirect('login')

            except (RuntimeError, TypeError, NameError, AttributeError):
                flash('Invalid Username or Password')
                return redirect('login')

#robots.txt

@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *Disallow: /get_flag"

#logout function
@app.route("/logout")
def logout():
    session["name"] = None
    flash("Logged Out")
    return redirect("login")


if __name__  == '__main__':
    app.run('0.0.0.0')
