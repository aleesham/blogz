from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8888/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


## Create our class
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String())

    def __init__(self, title, body):
        self.title = title
        self.body = body

def get_all_entries():
    return Blog.query.all()


## I need to edit new-post to effectively add blog posts. 
post1 = Blog("Post 1", "This is my post.")
post1.id = 1
post2 = Blog("Post 2", "This is my post.")
post2.id = 2
posts = [post1, post2]


## This needs to be edited
@app.route('/blog')
def index():
    blog_id = request.args.get('id')
    if blog_id:
        ## Change this to render the actual blog.
        return render_template('display-post.html', title = 'This works.', post=post)
    return render_template('blog.html', title = post.title, posts=posts)

    
@app.route('/newpost', methods = ['GET','POST'])
def post():
    
    return render_template('add-blog.html', title = 'Build-a-Blog')

if __name__ == '__main__':
    app.run()