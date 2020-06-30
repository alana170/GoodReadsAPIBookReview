from flask import Flask,  render_template, request
from flask_sqlalchemy import SQLAlchemy
import csv

#from sqlalchemy import create_engine
#from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book2.db'
db = SQLAlchemy(app)

class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key = True)
    Isbn = db.Column(db.String(100), unique = True)
    Title = db.Column(db.String(255), unique=True, nullable=False)
    Author = db.Column(db.String(255), unique=False, nullable=True)
    Year = db.Column(db.Integer, nullable= True) 

    def __repr__(self):
        return 'Book ID = ' + str(self.BookID)

@app.route('/')
def index(): 
    return render_template('books.html', books = Book.query.all())

@app.route('/uploadFile/')   
def uploadFile():
    f = open("C:/Users/sgoru/project1/project1/books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if(reader.line_num>1) : 
            new_book = Book(Isbn = isbn, Title = title, Author = author, Year = year)
            db.session.add(new_book) 
            db.session.commit()
    return 'File Uploaded'
    
@app.route('/book/<string: isbn>')
def ratingInfoByISBN():
    return 'Rating Info Goes Here'



"""
@app.route('/', method = ['POST', 'GET'])
def getValue():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
    else:
        return render_template('books.html')
 """  

if __name__=='__main__' :
    app.run(debug=True)


