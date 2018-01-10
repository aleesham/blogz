from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

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
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect('/login')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return 'Test'
    return render_template('signup.html', title='Signup')
    


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username = username).all()
        if len(existing_user) == 0:
            flash('Username does not exist.')
        elif existing_user[0].password != password:
            flash('Incorrect password.')
        else:
            session['username'] = username
            return redirect('/newpost')
    return render_template('login.html', title='Login')
 
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')

@app.route('/blog')
def displayAllBlogs():
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.filter_by(id = int(blog_id)).first()
        return render_template('blog.html', title = blog.title, blog=blog)
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
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id='+str(blog.id))

    return render_template('newpost.html', title="Add a Blog Entry")

if __name__ == '__main__':
    app.run()