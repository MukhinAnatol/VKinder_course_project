from db import *
from datetime import date


'''Функции для добавления информации в БД'''

#Сохранение данных пользователя
def insert_user(user_id, data):
    if user_id not in select_from_user():
        full_name = f"{data[0]['first_name']} {data[0]['last_name']}"
        city = data[0]['city']['id']
        birthday = data[0]['bdate'].split('.')
        user_age = date.today().year - int(birthday[-1])
        user_sex = data[0]['sex']
        new_user = Userinfo(user_name=full_name, vk_id=user_id, city_name=city, age=user_age, sex=user_sex)
        session.add(new_user)
        session.commit()
    else:
        pass

#Добавление в таблицу найденных пар для проверки на повторный вывод
def insert_match(user_id, match):
    db_id = connection.execute(f"""
                    SELECT id FROM userinfo
                    WHERE vk_id = {user_id};
                """).fetchone()[0]
    matches_db = select_from_match(db_id)
    dublicate_list = []
    for i in matches_db:
        dublicate_list.append(i[0])
    if match not in dublicate_list:
        new_match = Match(match_id=match,id_user=db_id)
        session.add(new_match)
        session.commit()
    else:
        pass

#Добавление в избранное
def insert_favourite(user_id, fav, data, photos):
    db_id = connection.execute(f"""
                        SELECT id FROM userinfo
                        WHERE vk_id = {user_id};
                    """).fetchone()[0]
    favourites = check_fav(db_id)
    if fav not in favourites:
        name = f"{data[0]['first_name']} {data[0]['last_name']}"
        link = 'https://vk.com/id' + str(fav)
        birthday = data[0]['bdate'].split('.')
        fav_age = date.today().year - int(birthday[-1])
        photos_str = '\n'.join(photos)
        new_fav = Favourite(fav_name=name, vk_id=fav, vk_link=link,
                            age=fav_age, photos=photos_str,id_user=db_id)
        session.add(new_fav)
        session.commit()
        return f'Пользователь был успешно добавлен в избранное'
    else:
        return f'Данный пользователь уже был добавлен в избранное'

