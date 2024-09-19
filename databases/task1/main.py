
from databases.task1.orm import DB


DB.create_tables()

# authors = [Author(name='newby'), Author(name='test')]
# genres = list(map(lambda x: Genre(name=x.capitalize()), 'history humour distopia fantasy sci-fi fiction'.split(' ')))
# DB.add_data(genres)
# DB.add_data(authors)
# for i in DB.get_data(Genre):
#     print(i)
