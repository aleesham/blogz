from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


## Create our class
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods = ['GET', 'POST'])
def index():
    blog_id = request.args.get('id')

    if request.method == 'POST':
        new_post_title = request.form['title'].strip()
        new_post_body = request.form['body'].strip()
        if (not new_post_title) or (not new_post_body):
            error = "Something went wrong. Please try again."
            return render_template('add-blog.html',  title = 'Build-a-Blog', post_title = new_post_title, post_body = new_post_body, error = error)
        post = Blog(new_post_title, new_post_body)
        db.session.add(post)
        db.session.commit()
        return redirect('/blog?id='+str(post.id))

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template('display-post.html', title = post.title, post = post)

    return render_template('blog.html', title = "Build-a-Blog", posts = Blog.query.all())

    
@app.route('/newpost')
def display():
    return render_template('add-blog.html', title = 'Build-a-Blog')


if __name__ == '__main__':
    app.run()