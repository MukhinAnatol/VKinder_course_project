import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

'''Работа с БД'''

#Имя пользователя БД, его пароль и название БД
db_user = ''
password = ''
db_name = ''

#Подключение к БД
db = f'postgresql://{db_user}:{password}@localhost:5432/{db_name}'
Base = declarative_base()
engine = sq.create_engine(db)
Session = sessionmaker(bind=engine)
session = Session()
engine.connect()
connection = engine.connect()

#Данные пользователя VK бота
class Userinfo(Base):
    __tablename__ = 'userinfo'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    user_name = sq.Column(sq.String)
    vk_id = sq.Column(sq.Integer)
    city_name = sq.Column(sq.String)
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)

#Данные найденных пары
class Match(Base):
    __tablename__ = '_match'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    match_id = sq.Column(sq.Integer)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('userinfo.id', ondelete='CASCADE'))

#Данные пар, добавленных в избранное
class Favourite(Base):
    __tablename__ = 'favourite'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    fav_name = sq.Column(sq.String)
    vk_id = sq.Column(sq.Integer, unique=True)
    vk_link = sq.Column(sq.String)
    age = sq.Column(sq.Integer)
    photos = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('userinfo.id', ondelete='CASCADE'))

'''Функции работы с БД'''

#Запрос на получение из БД vk_id пользователя
def select_from_user():
    users_id = connection.execute("""
        SELECT vk_id FROM userinfo;
    """).fetchall()
    id_list = []
    for item in users_id:
        one_id = item[0]
        id_list.append(one_id)
    return id_list

#Запрос на получение из БД id найденной пары с фильтром по vk_id пользователя
def select_from_match(user_id):
    match_ids = connection.execute(f"""
        SELECT match_id FROM _match
        WHERE id_user = {user_id};
    """).fetchall()
    id_list = []
    for item in match_ids:
        one_id = item
        id_list.append(one_id)
    return id_list

#Запрос на получение из БД id избранной пары с фильтром по vk_id пользователя
def check_fav(user_id):
    fav_ids = connection.execute(f"""
        SELECT vk_id FROM favourite
        WHERE id_user = {user_id};
    """).fetchall()
    id_list = []
    for item in fav_ids:
        one_id = item[0]
        id_list.append(one_id)
    return id_list

#Запрос на получение из БД списка избранных
def select_all_fav(user_id):
    db_id = connection.execute(f"""
                SELECT id FROM userinfo
                WHERE vk_id = {user_id};
            """).fetchone()[0]
    favourites = connection.execute(f"""
        SELECT fav_name, vk_link FROM favourite
        WHERE id_user = {db_id};
    """).fetchall()
    return favourites
