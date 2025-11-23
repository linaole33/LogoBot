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

#Открываю папку с учебными материалами
materials_folder = "materials"
if not os.path.exists(materials_folder):
    os.mkdir(materials_folder)  # создаём папку, если её нет

#Оставляем файл открытым на запись (указатель уже в конце)
#Событие на получение сообщения
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    #Создаю временную переменную для сравнения (чтобы строка сравнивалась со строкой)
    user_id_str = str(message.from_user.id)

    #Условие, есть ли такой юзер в списке пользователей
    if user_id_str in user_list:
         # Если пользователь уже есть — НЕ отправляем материалы повторно
     if user_id_str in user_list:
        bot.send_message(message.from_user.id, "Вы уже есть в списке пользователей.")
        return

    # Если пользователя нет — добавляем его + отправляем материалы
    users.write(user_id_str + "\n")
    user_list.append(user_id_str)

    bot.send_message(
        message.from_user.id,
        "Спасибо, добавил вас в список пользователей.\n"
        "Секунду, отправляю учебный материал…"
    )

    send_all_materials_to_user(message.from_user.id)

#Функция отправки всех материалов пользователю (только один раз)
def send_all_materials_to_user(user_id):

    sent_files = set()   # чтобы не отправлять один файл дважды

    #Бесконечный цикл проверки новых учебных материалов
    while True:

        #Получаем список файлов в папке (в массив)
        files = os.listdir(materials_folder)

        #Перебираем массив по одному
        for file_name in files:

            file_path = os.path.join(materials_folder, file_name)

            # Если файл уже отправляли — пропускаем
            if file_name in sent_files:
                continue

            #Определяем расширение файла
            ext = file_name.lower().split(".")[-1]

            for user in user_list:

                # === Картинки ===
                if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
                    f = open(file_path, "rb")
                    bot.send_photo(user, f)
                    f.close()

                # === Видео ===
                elif ext in ["mp4", "mov", "avi", "mkv"]:
                    f = open(file_path, "rb")
                    bot.send_video(user, f)
                    f.close()

                # === Документы ===
                else:
                    # PDF, DOC, DOCX, XLSX, PPTX, TXT и любые другие
                    f = open(file_path, "rb")
                    bot.send_document(user, f)
                    f.close()

            # Помечаем файл как отправленный
            sent_files.add(file_name)

        #Делаем паузу в 10 секунд
        time.sleep(10)
    # Запускаем функцию ожидания появления картинок в отдельном потоке
    threading.Thread(target=wait_for_images, daemon=True).start()

#Начинаю бесконечно слушать новые сообщения
bot.polling(none_stop=True, interval=0)

#Закрываю файл, который был открыт на запись
users.close()