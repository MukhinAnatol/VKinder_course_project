import vk_api
from random import randint
from db import select_from_match
from datetime import date

'''Функции поиска и сбора информации'''

#Работа с vk_api
community_token = "vk1.a.3jyrkg3Nhk4jzRbFz3A2DlfNNarrn8Z-wdis4HYB-XG1UzFQx06EZ9GivlUvWus2j0EKWjgcnWV555THEVKFKKAH9lK3OWrjYdZVoFUVuXMPXhbjaY53O9D8RBedqKIaC6a0bhwXYg3KBj9HZW6MIkXMnjCr6nBP_OlOnUnMEnPhTjE_KC8KUyCFRJhhNPdO"
my_token = ""

vk_session = vk_api.VkApi(token=community_token)
vk_my_session = vk_api.VkApi(token=my_token)
session_api = vk_session.get_api()


#Сбор информации пользователя для поиска подходящей пары
def get_user_info(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'sex, bdate, city, relation'
    }
    response = vk_session.method('users.get', params)
    return response


#Формирование полного имени пользователя
def get_user_name(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'sex, bdate, city, relation'
    }
    response = vk_session.method('users.get', params)
    full_name = f"{response[0]['first_name']} {response[0]['last_name']}"
    return full_name


#Поиск других пользователей по параметрам пользователя бота
def get_match(user):
    user_data = get_user_info(user)
    birthday = user_data[0]['bdate'].split('.')
    age = date.today().year - int(birthday[-1])
    city = user_data[0]['city']['id']
    sex = user_data[0]['sex']
    if sex == 2:
        sex = 1
    elif sex == 1:
        sex = 2
    params = {
        'sort': 0,
        'count': 1000,
        'city': city,
        'sex': sex,
        'status': 6,
        'age_from': age - 5,
        'age_to': age + 5,
        'has_photo': 1,
        'is_closed': False
    }
    response = vk_my_session.method('users.search', params)
    return response


#Поиск фотографий найденной пары
def get_photos(user, data):
    match = data['items'][randint(0, int(len(data['items']) - 1))]['id']
    message_data = {'name': '',
                    'id': match,
                    'link': None,
                    'photos': []}
    matches_db = select_from_match(user)
    if match in matches_db:
        return get_photos(user, data)
    else:
        params = {'owner_id': match,
              'album_id': 'profile',
              'extended': 1}
        try:
            photos = sorted(vk_my_session.method('photos.get', params)['items'],
                        key=lambda elem: elem['likes']['count'], reverse=True)[:3]
            message_data['name'] = f"{get_user_info(match)[0]['first_name']} {get_user_info(match)[0]['last_name']}"
            message_data['link'] = 'https://vk.com/id' + str(match)
            for photo in photos:
                photo_attachment = f'photo{str(match)}_{photo["id"]}'
                message_data['photos'].append(photo_attachment)
        except (Exception, vk_api.exceptions.ApiError):
            return get_photos(user, data)
        return message_data
