import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv
import requests


#engine = create_engine('mssql+pymssql://admin_Alana:1234@localhost:1433/Books')
#db = scoped_session(sessionmaker(bind=engine))

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "LwFswiQvej8jy0XQShrEA", "isbns": "9781632168146"})
print(res.json())

#f = open("books.csv")
#reader = csv.reader(f)
#for isbn, title, author, year in reader:
   # db.execute("INSERT INTO Book(Isbn, Title, Author, Year) VALUES ('"+isbn+"','"+title+"' , '"+author+ "','" +year + "')") 
 #   {"Isbn": isbn, "Title": title, "Author": author, "Year": year})
    #db.commit()



