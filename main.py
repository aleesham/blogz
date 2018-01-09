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

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog {0}>'.format(self.title)

@app.route('/blog')
def index():
    blog_id = request.args.get(id)
    if blog_id:
        print(blog_id)
        blog = Blog.query.filter_by(id = blog_id).first()
        return "Blog Added"
    return render_template('index.html',title='Build-a-Blog', blogs = Blog.query.all())

@app.route('/newpost', methods = ['GET','POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        #TODO Validation of the title and body instead of True
        if True:
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id='+str(blog.id))
        else:
            #TODO if not valid, redirect back to post page with errors
            continue

    return render_template('newpost.html', title="Add a Blog Entry")

if __name__ == '__main__':
    app.run()