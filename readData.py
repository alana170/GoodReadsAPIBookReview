import pyodbc, csv, requests, json

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-5DCQASK;'
                      'Database=Books;'
                      'Trusted_Connection=yes;')
 
cursor = conn.cursor()
f = open("C:/Users/sgoru/project1/project1/Books_test.csv")
reader = csv.reader(f)

for isbn, title, author, year in reader:
    if(reader.line_num>1) : 
        par = {"key": "LwFswiQvej8jy0XQShrEA", "isbns": isbn}
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params=par)
        s1 = ""
        s1 = res.json()
        data = json.dumps(s1)
        data_dict = json.loads(data)

        for item in data_dict['books']:
            # get info from goodreads and insert into sql table Book Ratings 
            sql = "INSERT INTO Books.dbo.BookRatingTable(id, isbn, isbn13, ratings_count, reviews_count, text_reviews_count, work_ratings_count, work_reviews_count, work_text_reviews_count, average_rating) VALUES (%d,'%s','%s',%d,%d,%d,%d,%d,%d,%s)" % (item['id'], item['isbn'], item['isbn13'], item['ratings_count'], item['reviews_count'], item['text_reviews_count'], item['work_ratings_count'], item['work_reviews_count'], item['work_text_reviews_count'], item['average_rating'])
            cursor.execute(sql)    
            cursor.commit()

cursor.close()
   




#for id, isbn, isbn13, ratings_count, reviews_count, text_reviews_count, work_ratings_count, work_reviews_count, work_text_reviews_count, average_rating in res.json():
     #cursor.execute("INSERT INTO BookRatingTable.dbo.Book () VALUES "+ "('"+isbn+"','"+title.replace("'","''")+"' , '"+author.replace("'","''") + "'," +year + ")")
#     print(id, isbn13)
     
conn.commit()





