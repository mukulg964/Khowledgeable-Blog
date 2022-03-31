from flask import Flask,render_template,request,redirect
from flask_login import LoginManager,login_user,UserMixin,logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='thisis'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    password = db.Column(db.String(80),nullable=False)
    fname = db.Column(db.String(80),nullable=False)
    lname = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),unique = True,nullable=False)
    username = db.Column(db.String(80),unique = True,nullable=False)


class Blog(db.Model):
    Blog_id =  db.Column(db.Integer,primary_key=True)
    title =  db.Column(db.String(80),nullable=False)
    author =  db.Column(db.String(80),nullable=False)
    content =  db.Column(db.String(80),nullable=False)
    pub_date =  db.Column(db.DateTime(),nullable=False,default = datetime.utcnow)
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    show = Blog.query.all()
    return render_template('index.html',show=show)


@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        user = User(email=email,password=password,fname=fname,lname=lname,username=username)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/')
        else:
            print('invalid')
            return redirect('login')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/blogpost',methods = ['GET','POST'])
def blogpost():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        show = Blog(title=title,author=author,content=content)
        db.session.add(show)
        db.session.commit()
        return redirect('/')
    return render_template('blogpost.html')

@app.route('/detail/<int:id>')
def detail(id):
    show = Blog.query.get(id)
    print(id)
    return render_template('detail.html',show=show)



@app.route('/delete/<int:id>')
def delete(id):
    data = Blog.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


@app.route('/edit/<int:id>',methods = ['GET','POST'])
def edit(id):
    show = Blog.query.get(id)
    if request.method == 'POST':
        show.title = request.form.get('title')
        show.author = request.form.get('author')
        show.content = request.form.get('content')
        db.session.commit()
        return redirect('/')
    return render_template('edit.html',show=show)





if __name__ == "__main__":
    app.run(debug = True,port=1000)
