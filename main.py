from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

entries=[]

class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body=db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body=body
        
    def __repr__(self):
        return '<Title %r>'  % self.title

def get_current_bloglist():
    return Entry.query.all()

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error_title = ''
        error_body = ''

        if not title:
            error_title = "Please fill in the title"
        if not body:
            error_body = "Please fill in the body"
        if not title or not body:
            return render_template('newpost.html',error_title=error_title, error_body=error_body)
        
        new_entry=Entry(title,body)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/blog?id={0}'.format(new_entry.id))
            
        
    return render_template('newpost.html',title="New Entry ")

@app.route('/blog', methods=["POST","GET"])
def blogs():
    if request.args:
        id=request.args.get('id')
        blogpost=Entry.query.get(id)
        title=blogpost.title
        body=blogpost.body
        return render_template('currentblog.html', title=title,body=body)
    else:
        return render_template('blog.html',title="What's Going On In The World",entries=get_current_bloglist())



if __name__=="__main__":
    app.run()