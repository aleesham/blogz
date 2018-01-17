from flask import Flask, redirect, render_template, request, session, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'y337kGcys&zP3B'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(3000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ### TODO add a DateTime column eventually so we can sort with respect to it.

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Blog {0}>'.format(self.title)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'list_blogs', 'index']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect('/login')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        existing_user = User.query.filter_by(username = username).all()
        if len(existing_user):
            flash('Username already exists.', 'error')
        if len(username)*len(password)*len(verify_password) == 0:
            flash('One or more fields left empty.', 'error')
        if len(username)<3 or len(username)>20 or len(password)<3 or len(password)>20:
            flash('Invalid username or password.', 'error')
        if password != verify_password:
            flash('Passwords do not match.', 'error')
        if len(get_flashed_messages()) == 0:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
    return render_template('signup.html', title='Sign Up')
    


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username = username).all()
        if len(existing_user) == 0:
            flash('Username does not exist.', 'error')
        else:
            pw_hash = existing_user[0].pw_hash.split(',')[0]
            salt = existing_user[0].pw_hash.split(',')[1]
            if pw_hash != check_pw_hash(password, salt):
                flash('Incorrect password.', 'error')
        if len(get_flashed_messages()):
            return redirect('/login')  # This conditional is unnecessary with the way the code is written but the instructions ask to redirect.
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect('/newpost')
    return render_template('login.html', title='Login')
 
@app.route('/logout')
def logout():
    flash('Logged out.')
    del session['username']
    return redirect('/blog')

@app.route('/')
def index():
    return render_template('index.html', title='Users', users=User.query.all())

@app.route('/blog')
def list_blogs():
    blog_id = request.args.get('id')
    user_id = request.args.get('user_id')
    if blog_id:
        blog = Blog.query.filter_by(id=int(blog_id)).first()
        return render_template('singleBlog.html', title = blog.title, blog=blog)
    if user_id:
        owner = User.query.filter_by(id=int(user_id)).first()
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('singleUser.html', title = "Blogs by " + owner.username, blogs=blogs)
    blogs = Blog.query.all()
    blogs.reverse()
    return render_template('displayBlogs.html',title='Build-a-Blog', blogs = blogs)

@app.route('/newpost', methods = ['GET','POST'])
def post():
    if request.method == 'POST':
        title = request.form['title'].strip()
        body = request.form['body'].strip()
        title_error = ''
        body_error = ''
    
        if title == '' or body == '':
            if title == '':
                title_error = 'Please fill in the title'

            if body == '':
                body_error = 'Please fill in the body'

            return render_template('newpost.html', title="Add a Blog Entry", blog_title = title, title_error = title_error, body = body, body_error = body_error)
            
        else:
            blog = Blog(title, body, User.query.filter_by(username = session['username']).first())
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id='+str(blog.id))

    return render_template('newpost.html', title="Add a Blog Entry")

if __name__ == '__main__':
    app.run()