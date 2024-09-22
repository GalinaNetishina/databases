from models import *
from databases.task1.orm import DB


DB.create_tables()

# DB.fill_with_fake()
for i in DB.all_books():
    print(i, i.author, i.genre)
for i in DB.books_dto():
    print(i)
