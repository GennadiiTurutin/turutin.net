from flask import render_template, redirect, request, url_for, flash, Blueprint, session, current_app
from flask_login import login_user, logout_user, current_user
from app import decorators
from app import db, mail
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, RequestForm, ForgotPasswordForm
from flask_mail import Message
import requests 
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from decouple import config

auth = Blueprint('auth', __name__)

def send_simple_message(email, subject, text):
    app = current_app._get_current_object() 
    return requests.post(
        app.config['MAIL_HOST_URL'],
        auth=("api", app.config['MAIL_HOST_PASSWORD']),
        data={"from": app.config['MAIL_HOST_USER'],
            "to": [email],
            "subject": subject,
            "text": text})

def manage_prev_page():
    global session, request
    if 'profile' not in request.referrer and 'change_password' not in request.referrer \
    and 'forgot_password' not in request.referrer \
    and 'login' not in request.referrer \
    and 'register' not in request.referrer \
    and 'request_password'  not in request.referrer:
        session['prev_page'] = request.referrer

@auth.route('/back', methods=['GET'])
def back():
    if session['prev_page']:
        return redirect(session['prev_page'])
    else: 
        return redirect(url_for('main.blog'))

@auth.route('/reroute', methods=['GET'])
def reroute():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    else: 
        return redirect(url_for('auth.login'))

@auth.route('/reroute_logout', methods=['GET'])
def reroute_logout():
    if not current_user.is_authenticated:
        flash("You cannot log out, as you are not logged in")
    else: 
        return redirect(url_for('auth.logout'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        manage_prev_page()
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("You've been logged in")
            return redirect(session['prev_page'])
        else:
            flash('Login Unsuccessful. Please check email and password')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    if request.method == 'GET':
        manage_prev_page()

    if current_user.is_authenticated:
        flash('You have been logged out')
        logout_user()
        return redirect(session['prev_page'])
    flash("You cannot log out, as you are not logged in")
    return redirect(session['prev_page'])


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        manage_prev_page()
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(session['prev_page'])
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        send_simple_message(user.email, "Registration turutin.net", 
            "Your account has been created successfully.")
        flash('Your account has been created!')
        return redirect(session['prev_page'])
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        manage_prev_page()
    form = RequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.get_reset_password_token()
            link = "http://127.0.0.1:5000/auth/reset_password/" + token
            send_simple_message(user.email, "Password reset turutin.net", link )
            flash("We've sent you an email with the link to reset your password")
            return redirect(session['prev_page'])
        else: 
            flash("Please check your email")
    return render_template('auth/request_password.html', form=form)

@auth.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    #if request.method == 'GET':
        #manage_prev_page()
    form = ForgotPasswordForm()
    user = User.verify_reset_password_token(token)
    if request.method == 'GET':
        if not user:
            flash('You are not authorized')
            return redirect(session['prev_page'])
        else:
            if form.validate_on_submit():
                user.set_password(form.newpassword.data)
                db.session.commit()
                flash('Your password has been reset')
                return redirect(url_for('auth.login'))
            else: 
                flash('Check your credentials')
    return render_template('auth/forgot_password.html', form=form, token=token)


@auth.route('/change_password', methods=['GET', 'POST'])
@decorators.login_required
def change_password():
    if request.method == 'GET':
        manage_prev_page()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.oldpassword.data) and \
        form.newpassword.data == form.confirmation.data:
            current_user.set_password(form.newpassword.data)
            db.session.commit()
            flash('Your password has been updated')
            return redirect(session['prev_page'])
        else: 
            flash('Please check your credentials')
    return render_template("auth/change_password.html", form=form)

