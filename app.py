import requests, json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import csv
from datetime import datetime
from sqlalchemy import or_, func 
import datetime

app = Flask(__name__)
app.secret_key = 'alana170project1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book3.db'
db = SQLAlchemy(app)

class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key = True)
    Isbn = db.Column(db.String(100), unique = False)
    Title = db.Column(db.String(255), unique=False, nullable=False)
    Author = db.Column(db.String(255), unique=False, nullable=True)
    Year = db.Column(db.Integer, nullable= True) 

    def __repr__(self):
        return 'Book ID = ' + str(self.BookID)

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key = True)
    Email = db.Column(db.String(100), unique=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(50), unique=False, nullable=False)
    Created = db.Column(db.DateTime())

    def __repr__(self):
        return 'User ID = ' + str(self.UserID)

class Review(db.Model):
    BookID = db.Column(db.Integer())
    ReviewID = db.Column(db.Integer(), primary_key = True)
    Username = db.Column(db.String(50), nullable=False)
    RatingNumber = db.Column(db.Integer(), nullable=False, default=0)
    Opinion = db.Column(db.String(2000))
    Created = db.Column(db.DateTime())


@app.route('/books', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
    if request.method == 'POST':
        mesg = ''
        if request.form['search'] != '':
            results = Book.query.filter(or_(Book.Title.like("%" +request.form['search'] + "%"),
            Book.Author.like("%" + request.form['search'] + "%"),
            Book.Isbn.like("%" + request.form['search'] + "%"))).all() 
            if Book.query.filter(or_(Book.Title.like("%" + request.form['search'] + "%"),
            Book.Author.like("%" + request.form['search'] + "%"),
            Book.Isbn.like("%" + request.form['search'] + "%"))).count() == 0: 
                mesg = "No search results found"
            return render_template('books.html', books = results, message = mesg)
        else:
            return redirect(url_for('index'))
    return render_template('books.html', books = Book.query.all(), message = "")


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST' :
        if request.form['username'] != "" and request.form['password'] != "" :
            if db.session.query(User).filter_by(Username = request.form['username']).count() != 0 : 
                user = db.session.query(User).filter_by(Username = request.form['username']).one()
                if user.Password == request.form['password'] :
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = 'Invalid Credentials. Please try again.'
            else:
                error = "Invalid Credentrial. Please try again."
        else:
            error = "Please Enter Values"
    
    return render_template('login.html', error = error)

@app.route('/uploadFile')   
def uploadFile():
    f = open("C:/Users/sgoru/project1/project1/books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if reader.line_num>1 : 
            if db.session.query(Book).filter_by(Isbn = isbn) == None:
                new_book = Book(Isbn = isbn, Title = title, Author = author, Year = year)
                db.session.add(new_book) 
                db.session.commit()
    return 'File Uploaded'
    
@app.route('/book/<Isbn>', methods=['GET', 'POST'])
def ratingInfoByISBN(Isbn):
    flag = False
    username = "anonymous" 
    if 'username' in session:
        username = session['username']
    bookid = db.session.query(Book).filter_by(Isbn = Isbn).first().BookID
    if request.method == "POST" :
        new_review = Review(BookID = bookid, Username= username , RatingNumber= request.form['opt'], Opinion= request.form['opinion'], Created = datetime.datetime.now() )
        db.session.add(new_review) 
        db.session.commit()
    avg = int(0)
    bookInfo= db.session.query(Book).filter_by(Isbn = Isbn).first() 
    errM = "" 
    par = {"key": "LwFswiQvej8jy0XQShrEA", "isbns": Isbn}
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params=par)          
        s1 = ""
        s1 = res.json()
        data = json.dumps(s1)
        data_dict = json.loads(data)
        avg = int(float(data_dict['books'][0]['average_rating']))
    except Exception as err:
        errM = repr(err)

    Reviews = db.session.query(Review).filter_by(BookID = bookid).all()
    for review in Reviews:
        if review.Created is not None : 
            t = review.Created
            review.Created = t.strftime('%m/%d/%Y %I:%M %p')
        else:
            review.Created = ""
        if review.Username == username:
            flag = True
        
    return render_template('ratings.html', data = s1, errM = errM, bookInfo = bookInfo, avg=avg, reviews = Reviews, reviewedflag = flag)

@app.route('/signup', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        if db.session.query(User).filter_by(Username = request.form['username']).one() is not None :
            message = "Username already exists"
            return render_template('signup.html', message = message)
        else:
            new_user = User(
            Email =request.form['email'], 
            Username = request.form['username'],
            Password = request.form['password'],
            Created = datetime.datetime.now())
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    else: 
        return render_template('signup.html', message= "")

@app.route('/logout')
def logout() : 
    username = "anonymous"
    if 'username' in session:
        username = session['username']
        mesg = username + " has successfully logged out."
        session.pop('username', None)
    return render_template('logout.html', message = mesg)

@app.route('/api/<Isbn>', methods=['GET', 'POST'])
def apiAccess():
    if request.method == "GET" : 
        



if __name__=='__main__' :
    app.run(debug=True)


