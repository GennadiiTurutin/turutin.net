from flask import Flask, render_template, request, session, make_response, jsonify, redirect, url_for, flash
from slugify import slugify
from database import Database
from user import User
from blog import Blog
import decorators

app = Flask(__name__)
app.secret_key = 'Gennadii'


@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def homepage():
    posts = Blog.get_all_posts()
    return render_template('homepage.html', posts=posts, slugify=slugify)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
@decorators.login_required
def logout():
    session['logged_in'] = False
    session['name'] = None
    flash("You have been logged out", category="success")
    return redirect(url_for('homepage'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/auth/login', methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.login_valid(email, password):
            User.login(email)
            session['logged_in'] = True
            session['name'] = email
            flash("You've been logged in", category='success')   
            return redirect(url_for('homepage'))
        else:
            flash("Wrong password or email!", category='warning')   
            return redirect(url_for('login'))


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    confirmation = request.form['confirmation']
    if password == confirmation:
        if User.register(email, password):
            session['logged_in'] = True
            session['name'] = email
            flash("You've got registered", category='success' )
            return redirect(url_for('homepage'))
        else:
            flash("The user with this email already exists", category='warning' )
            return redirect(url_for('register'))
    else: 
        flash("Please check password", category='warning')
        return redirect(url_for('register'))


@app.route('/profile')
@decorators.login_required
def profile():
    obj = User.get_data 
    return render_template('profile.html', obj=obj)


@app.route('/post/<int:post_id>/<string:post_url>')
def post(post_id, post_url):
    post = Blog.get_by_id(_id=post_id)
    return render_template('post.html', post=post)

@app.route('/add')
@decorators.admin_required
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
@decorators.admin_required
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    post = Blog(title, subtitle, author, content)
    post.add()
    flash("You've created a new post", category='success' )
    return redirect(url_for('homepage'))

@app.route('/deletepost/<int:post_id>', methods=['GET'])
@decorators.admin_required
def deletepost(post_id):
    Blog.delete(post_id)
    flash("You've deleted the post", category='success' )
    return redirect(url_for('homepage'))

@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
@decorators.admin_required
def editpost(post_id):

    if request.method == 'GET':
        post = Blog.get_by_id(_id=post_id)
        return render_template("edit_post.html", post=post, post_id=post_id)

    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        author = request.form['author']
        content = request.form['content']
        Blog.edit(post_id, title, subtitle, author, content)
        flash("You've edited the post", category='success' )
        return redirect(url_for('homepage'))
    
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Error 404"), 404 


@app.errorhandler(504)
def error_504(e):
    return render_template('error.html', error="Error 504. Something is wrong with Quandl"), 504 


@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error="Error 500. Server error"), 500   


if __name__== '__main__':
    app.run(port=5000, debug=True)



