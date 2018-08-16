from functools import wraps
from flask_login import current_user
from flask import url_for, redirect, flash

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated == True:
            return func(*args, **kwargs)
        else:
            flash("You need to log in first", category='warning')
            return redirect(url_for('auth.login'))
    return wrap

def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        #if session['name'] == "gennadii.turutin@gmail.com":
        return func(*args, **kwargs)
        #else:
        #flash("Access restricted", category='warning')
         #   return redirect(url_for('homepage'))
    return wrap