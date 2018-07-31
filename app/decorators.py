from functools import wraps
from flask import session, url_for, redirect, request, flash

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if session['logged_in'] == True:
            return func(*args, **kwargs)
        else:
            flash("You need to login first", category='warning')
            return redirect(url_for('login'))
    return wrap

def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if session['name'] == "gennadii.turutin@gmail.com":
            return func(*args, **kwargs)
        else:
            flash("Access restricted", category='warning')
            return redirect(url_for('homepage'))
    return wrap