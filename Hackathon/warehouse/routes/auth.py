# auth.py
import sys
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from warehouse import Backend, db
from user import User
auth = Blueprint('auth', __name__)

'''
Login to catch already logged in users
'''
@auth.route('/login')
def login():
    if current_user != None and current_user.is_authenticated:
        if current_user.isManager():
            return redirect(url_for("main.managerHomepage"))
        elif current_user.isAdmin():
            return redirect(url_for("main.adminHomepage"))
    return render_template("loginPage.html")

@auth.route('/login', methods=['POST'])
def login_post():
    if current_user != None and current_user.is_authenticated:
        if current_user.isManager():
            return redirect(url_for("main.managerHomepage"))
        elif current_user.isAdmin():
            return redirect(url_for("main.adminHomepage"))

    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User(username)

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if user.password == "" or not check_password_hash(user.password, password):
        db.db.Logins.update({"ID":user.id}, {"$inc" : {"attempts":1}})
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    if db.db.Logins.find({"ID":user.id}).next()["attempts"] >= 20:
        flash("Too many login attempts, contact an administrator")
        return redirect(url_for('auth.login'))
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    if user.isManager():
        return redirect(url_for('main.managerHomepage'))
    elif user.isAdmin():
        return redirect(url_for('main.adminHomepage'))


@auth.route('/createAccount', methods=['POST'])
def createAccount():
    # Get form data
    name = request.form.get("name")
    userName = request.form.get("username")
    hashedPassword = generate_password_hash(request.form.get("password"), method='sha256')
    accType = request.form.get("type")
    sections = []
    for section in Backend.getSections():
        if request.form.get(section["Name"]) != None:
            sections.append(section["ID"])
    Backend.createAccount(name, userName, hashedPassword, accType, sections)
    return '', 204

@auth.route('/deleteAccount', methods=['POST'])
def deleteAccount():
    # Get form data
    ID = request.form.get("ID")
    Backend.deleteAccount(ID)
    return '', 204

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login_page'))