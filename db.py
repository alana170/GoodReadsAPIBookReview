import sqlite3
import csv 

connection = sqlite3.connect('db/book.db')
cursor = connection.cursor()

sql = ''' CREATE TABLE IF NOT EXISTS Book
            (BookID INTEGER PRIMARY KEY AUTOINCREMENT,
	        Isbn varchar(100),
	        Title varchar(255) ,
	        Author varchar(255) ,
	        Year INTEGER)'''
cursor.execute(sql)

f = open("C:/Users/sgoru/project1/project1/books.csv")
reader = csv.reader(f)

for isbn, title, author, year in reader:
    if(reader.line_num>1) : 
        sql3 = "INSERT INTO Book (Isbn, Title, Author, Year) VALUES ('" + isbn + "','" + title.replace("'", "''") + "','" + author.replace("'", "''") + "',"  + year + ")"
        cursor.execute(sql3)
        connection.commit()


sql2 = 'SELECT * FROM Book'
cursor.execute(sql2)

rows = cursor.fetchall()
for row in rows:
    print(row)

connection.close()



