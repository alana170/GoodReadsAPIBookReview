from flask import Flask,  render_template, request
from flask_sqlalchemy import SQLAlchemy

#from sqlalchemy import create_engine
#from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db = SQLAlchemy(app)

class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key = True)
    Isbn = db.Column(db.String(100), unique = True)
    Title = db.Column(db.String(255), unique=True, nullable=False)
    Author = db.Column(db.String(255), unique=False, nullable=True)
    Year = db.Column(db.Integer, nullable= True) 

    def __repr__(self):
        return 'Book ID = ' + str(self.BookID)


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


