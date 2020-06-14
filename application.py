import os

from flask import Flask, render_template, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from forms_fiels import *
from models import *

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    return "Hey welcome"


@app.route("/logout", methods = ['GET', 'POST'])
def logout():

    logout_user()
    flash("Logged out successfully!!", 'success')

    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug = True)