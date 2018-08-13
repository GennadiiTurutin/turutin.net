from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from app import db, mail
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from flask_mail import Message
from app import mail

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash("You've been logged in")
            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        flash('You have been logged out.')
        logout_user()
        return redirect(url_for('main.homepage'))
    flash("You cannot log out, as you are not logged in")
    return redirect(url_for('main.homepage'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    if form.validate_on_submit():
        
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
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

@auth.route('/forgot_password')
def forgot_password():
    msg = Message("Please use this link to change this password",
                      sender="gennadii.turutin@gmail.com",
                      recipients=["gennadii.turutin@gmail.com"])
    mail.send(msg)
    return redirect(url_for('main.homepage'))

@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
    return render_template("auth/change_password.html", form=form)


