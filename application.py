import os

from flask import Flask, render_template, redirect, url_for, flash, request
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import pandas as pd

from forms_fiels import *
from models import *
from project import *

app = Flask(__name__)
app.secret_key = 'K\xa6\x13\x94\xeex\x06\xf6 \xf6K&\xef\xd8\x160\xb8\x18u\xae"2D8'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nzolhcsgkxnend:ce453464e459b09167422b0bc451957846c8b7a682d5ef7480799320bc0c342f@ec2-3-231-16-122.compute-1.amazonaws.com:5432/d5qu4f6kvlnuon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'myfolder'

db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    
    return User.query.get(int(id))

@app.route("/", methods = ['GET', 'POST'])
def index():

    reg_form = Registration()

    if reg_form.validate_on_submit():
        
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        user = User(username = username, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Registered Successfully!!", 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form = reg_form)

@app.route("/login", methods = ['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        
        user_object = User.query.filter_by(username = login_form.username.data).first()
        login_user(user_object)

        return redirect(url_for('main'))

    return render_template("login.html", form = login_form)


@app.route("/main", methods = ['GET', 'POST'])
#@login_required
def main():

    if not current_user.is_authenticated:

        flash("Please Login", 'danger')
        return redirect(url_for('login'))

    return render_template("main.html")

@app.route("/logout", methods = ['GET', 'POST'])
def logout():

    logout_user()
    flash("Logged out successfully!!", 'success')

    return render_template("logout.html")

@app.route('/success', methods=['GET', 'POST'])
def success():

    if request.method == 'POST':

        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        l = 'myfolder/{}'.format(f.filename)

        return readfile(l)

    return render_template("main.html")

@app.route('/success2', methods=['GET', 'POST'])
def success2():

    if request.method == 'POST':

        f1 = request.files['file1']
        f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename))
        f2 = request.files['file2']
        f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))

        l1 = 'myfolder/{}'.format(f1.filename)
        l2 = 'myfolder/{}'.format(f2.filename)

        return arrangement(l1, l2)

    return render_template("main.html")

if __name__ == "__main__":

    app.run(debug = True)