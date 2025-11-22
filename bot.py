import telebot;
bot = telebot.TeleBot('8020115600:AAEuWDPnVxRkT2H_1HA7G_Ar7rZ1g7K0WvE');

#Считываю в массив user_list список пользователей из файла
user_list = []
users = open("users.txt", "a+", encoding="utf-8")  # a+ — открыть на чтение/дозапись, создать если нет
users.seek(0)  # переходим в начало файла, чтобы прочитать содержимое

for line in users:
    user_list.append(line.strip())

#Оставляем файл открытым на запись (указатель уже в конце)
#Событие на получение сообщения
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    #Создаю временную переменную для сравнения (чтобы строка сравнивалась со строкой)
    user_id_str = str(message.from_user.id)

    #Условие, есть ли такой юзер в списке пользователей
    if user_id_str in user_list:
        #Если есть, просто отвечаем, что он уже есть
        bot.send_message(message.from_user.id, "Вы уже есть в списке пользователей.")
    else:
        #Если нет, дописываю id пользователя в файл
        users.write(user_id_str + "\n")
        user_list.append(user_id_str)

        #И отвечаю пользователю
        bot.send_message(
            message.from_user.id,
            "Спасибо, добавил вас в список пользователей. "
            "Вы получите учебный материал, как только он будет отправлен администратором."
        )

#Начинаю бесконечно слушать новые сообщения
bot.polling(none_stop=True, interval=0)

#Закрываю файл, который был открыт на запись
users.close()