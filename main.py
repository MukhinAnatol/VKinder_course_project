from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from insert_db import insert_user, insert_match, insert_favourite, Base, engine
from db import select_all_fav
from api_vk import get_match, get_photos, get_user_info, get_user_name, vk_session
import time


'''Работа с VK ботом'''

longpoll = VkLongPoll(vk_session)


#Функция для общения VK бота с пользователем
def write_msg(user_id, message=None, attachment=None):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment, 'random_id': randrange(10 ** 7)})


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()
                #Приветствуем пользователя, обращаясь к нему полным именем и выводим команды
                if request == "привет":
                    write_msg(event.user_id, f"Хай, {get_user_name(event.user_id)}"
                                             f"\nКоманда для поиска пары: далее"
                                             f"\nКоманда для выхода из программы: стоп")
                elif request == 'стоп':
                    write_msg(event.user_id, "Пока((")
                    break
                #Ищем пару
                elif request == "далее":
                    user_data = get_user_info(event.user_id)
                    insert_user(event.user_id, user_data)
                    matches = get_match(event.user_id)
                    result = get_photos(event.user_id, matches)
                    match = result['id']
                    photos = result['photos']
                    insert_match(event.user_id, match)
                    #Выводим пользователю информацию о найденной паре
                    write_msg(event.user_id, f"{result['name']}"
                                             f"\n{result['link']}")
                    for index, item in enumerate(photos):
                        write_msg(event.user_id, message=None, attachment=photos[index])
                    time.sleep(2)
                    write_msg(event.user_id, f"Команда для продолжения: далее"
                                             f"\nКоманда для добавления в избранное: добавить в избранное"
                                             f"\nКоманда для просмотра избранных: избранные")
                #Добавляем в избранное
                elif request == "добавить в избранное":
                    fav_data = get_user_info(match)
                    message = insert_favourite(event.user_id, match, fav_data, photos)
                    write_msg(event.user_id, f'{message}')
                #Выводим избранные
                elif request == "избранные":
                    favourites = select_all_fav(event.user_id)
                    write_msg(event.user_id, f'Избранные пользователи:')
                    for fav in favourites:
                        write_msg(event.user_id, f'{fav[0]}, {fav[1]}')
                #Предупреждаем пользователя о неправильной команде
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")

