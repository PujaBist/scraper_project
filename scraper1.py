#go to  git bash
# git config --global user.name "puja bist"
#git config --global uer.email "bistpuja71@gmail.com"


#git init =>intialize git
#git status => if you want to check what are the status of files
#git diff => if you want to check what are the changes
# git add . => trcak all files
#git commit =>"your message"

############
# 1.change the code
# 2. git add .
# 3. git commit -m "Your message"
# 4. git push
##################


  import json
import requests 
from bs4 import BeautifulSoup 
import sqlite3

URL="http://books.toscrape.com/"
def create_table():
  con=sqlite3.connect("books.sqlite3")
  cur=con.cursor()
  cur.execute(
      """
    CREATE TABLE  if  not exists books(
      id integer primary key autoincrement,
      title text,
      currency text,
      price real);
      """
    )
  con.commit()
  con.close()
def insert_book(title,currency,price):
  conn=sqlite3.connect("books.sqlite3")
  cursor=conn.cursor()
  cursor.execute("INSERT INTO books(title,currency,price) VALUES (?,?,?)",
    (title,currency,price),
    )
  conn.commit()
  conn.close()


def scrape_books(url) :
  response=requests.get(url)
  #print(response) # same way to get requests
  # another waay to get requests
  #print(response.status_code)
  if response.status_code != 200 :
    return []

  books=[]

    # set encoding explicily to handle special characters correctly
  response.encoding=response.apparent_encoding
  #print(response.text)
  soup = BeautifulSoup(response.text,"html.parser")
  book_elements=soup.find_all("article",class_="product_pod")
  #print(book_elements)
  for book in book_elements :
    title=book.h3.a['title']
    price_text=book.find("p", class_="price_color").text
    currency=price_text[0]
    price=price_text[1:]
    books.append(
      {

      "title":title,
    "currency":currency,
    "price":price,}
    )
   # print(title,currency,price)
    #insert_book(title,currency,price)
  

  print("All books have been scrapped and saved to the database.")
  return books


def save_to_json(books):

  with open("books.json","w",encoding="utf-8") as f :
    json.dump(books, f,indent=4,ensure_ascii=False)

  print("all books have been saved to json")


create_table() 

books=scrape_books(URL)

save_to_json(books)

