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


### Everything works. Now go back and actually read the directions to see if everything works. Also I feel like this route can be done better, but I'm not really sure how just yet. 
@app.route('/blog', methods = ['GET', 'POST'])
def index():
    blog_id = request.args.get('id')

    if request.method == 'POST':
        new_post_title = request.form['title']
        new_post_body = request.form['body']
        post = Blog(new_post_title, new_post_body)
        db.session.add(post)
        db.session.commit()

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template('display-post.html', post = post)

    return render_template('blog.html', title = "Build-a-Blog", posts=Blog.query.all())

    
@app.route('/newpost', methods = ['GET', 'POST'])
def display():
    new_action = "/blog?id=" + str(len(Blog.query.all()) + 1)
    return render_template('add-blog.html', new_action = new_action, title = 'Build-a-Blog')


if __name__ == '__main__':
    app.run()