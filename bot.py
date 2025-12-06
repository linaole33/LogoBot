#Подключаю модуль для работы с ТГ
import telebot

#Подключаю модуль для работы с папками
import os

#Подключаю модуль для возможности паузы
import time

#Подключаю модуль, который может запустить отдельный поток программы
import threading

bot = telebot.TeleBot('8020115600:AAEuWDPnVxRkT2H_1HA7G_Ar7rZ1g7K0WvE');

#Считываю в массив user_list список пользователей из файла
user_list = []
users = open("users.txt", "a+", encoding="utf-8")  # a+ — открыть на чтение/дозапись, создать если нет
users.seek(0)  # переходим в начало файла, чтобы прочитать содержимое

for line in users:
    user_list.append(line.strip())

#Список отправленных файлов
sent_files_list = []
sent_files = open("sent_files.txt", "a+", encoding="utf-8")
sent_files.seek(0)

for line in sent_files:
    sent_files_list.append(line.strip())

#Открываю папку с учебными материалами
materials_folder = "../materials"
if not os.path.exists(materials_folder):
    os.mkdir(materials_folder)  # создаём папку, если её нет

#Оставляем файл открытым на запись (указатель уже в конце)
#Событие на получение сообщения
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    member = bot.get_chat_member(-1002132817329, message.from_user.id)
    if member.status in ['member', 'administrator', 'creator']:
        #Создаю временную переменную для сравнения (чтобы строка сравнивалась со строкой)
        user_id_str = str(message.from_user.id)

        #Условие, есть ли такой юзер в списке пользователей
        if user_id_str in user_list:
            bot.send_message(message.from_user.id, "Вы уже есть в списке пользователей.")
        else:
            # Добавляем нового пользователя
            users.write(user_id_str + "\n")
            users.flush()
            user_list.append(user_id_str)

            bot.send_message(
                message.from_user.id,
                "Спасибо, добавил вас в список пользователей.\n"
                "Отправляю доступные материалы…"
            )

            # Отправляем новому пользователю все материалы, которые еще не отправлялись никому
            files = os.listdir(materials_folder)
            for file_name in files:
                if file_name not in sent_files_list:
                    file_path = os.path.join(materials_folder, file_name)
                    send_file_to_user(message.from_user.id, file_path)
    else:
        bot.send_message(
            message.from_user.id,
            "Чтобы получить материалы, подпишитесь на канал https://t.me/kseniasadko"
        )



# === Универсальная отправка файла пользователю ===
def send_file_to_user(user_id, file_path):
    ext = file_path.lower().split(".")[-1]

    if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
        f = open(file_path, "rb")
        bot.send_photo(user_id, f)
        f.close()

    elif ext in ["mp4", "mov", "avi", "mkv"]:
        f = open(file_path, "rb")
        bot.send_video(user_id, f)
        f.close()

    else:
        f = open(file_path, "rb")
        bot.send_document(user_id, f)
        f.close()

# === Функция: проверить папку и отправить НОВЫЕ материалы ВСЕМ пользователям ===
def scan_for_new_materials():
    while True:
        files = os.listdir(materials_folder)
        for file_name in files:

            # Новый ли это материал?
            if file_name not in sent_files_list:

                file_path = os.path.join(materials_folder, file_name)

                # Отправляем всем пользователям
                for user in user_list:
                    send_file_to_user(user, file_path)

                # Записываем, что файл отправлен
                sent_files.write(file_name + "\n")
                sent_files.flush()   # чтобы сохранить сразу
                sent_files_list.append(file_name)

        time.sleep(10)


# Запускаем функцию ожидания появления картинок в отдельном потоке
threading.Thread(target=scan_for_new_materials, daemon=True).start()

#Начинаю бесконечно слушать новые сообщения
bot.polling(none_stop=True, interval=0)

#Закрываю файл, который был открыт на запись
users.close()