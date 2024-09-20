from models import *
from databases.task1.orm import DB


DB.create_tables()

# DB.fill_with_fake()
for i in DB.get_data():
    print(i, i.author, i.genre)
