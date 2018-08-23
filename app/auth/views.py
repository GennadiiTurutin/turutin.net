from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import login_user, logout_user, current_user
from app import decorators
from app import db, mail
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, RequestForm, ForgotPasswordForm
from flask_mail import Message
from app import mail
from app.models import User 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("You've been logged in", 'success')
            return redirect(url_for('main.homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'warning')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
@decorators.login_required
def logout():
    if current_user.is_authenticated:
        flash('You have been logged out.', 'success')
        logout_user()
        return redirect(url_for('main.homepage'))
    flash("You cannot log out, as you are not logged in", 'warning')
    return redirect(url_for('main.homepage'))


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        msg = Message("You've been successfully registered! Welcome!",
                      sender="gennadii.turutin@gmail.com",
                      recipients=["gennadii.turutin@gmail.com"])
        mail.send(msg)
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = RequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.get_reset_password_token()
            msg = Message("Please use this link to change this password",
                          sender="gennadii.turutin@gmail.com",
                          recipients=["gennadii.turutin@gmail.com"])
            msg.html = render_template('email/reset_password.html', user=user, token=token)
            mail.send(msg)
            flash("We've sent you an email with the link to reset your password", 'info')
            return redirect(url_for('main.homepage'))
        else: 
            flash("Please check your email", 'info')
    return render_template('auth/request_password.html', form=form)


@auth.route('/forgot_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ForgotPasswordForm()
    user = User.verify_reset_password_token(token)
    if request.method == 'POST':
        if not user:
            flash('You are not authorized', 'info')
            return redirect(url_for('main.homepage'))
        else:
            if form.validate_on_submit():
                user.set_password(form.newpassword.data)
                db.session.commit()
                flash('Your password has been reset.', 'success')
                return redirect(url_for('auth.login'))
            else: 
                flash('Check your data', 'info')
    return render_template('auth/forgot_password.html', form=form, token=token)


@auth.route('/change_password', methods=['GET', 'POST'])
@decorators.login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
            if current_user.check_password(form.oldpassword.data):
                current_user.set_password(form.newpassword.data)
                db.session.commit()
                flash('Your password has been updated.', 'success')
                return redirect(url_for('main.homepage'))
            else: 
                flash('Please check your password', 'warning')
    return render_template("auth/change_password.html", form=form)

