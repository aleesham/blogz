from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(3000))
    ### TODO add a DateTime column eventually so we can sort with respect to it.

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog {0}>'.format(self.title)

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