from config import config_read, admin, to_slovar
from telebot import types, TeleBot
from email_addres import email, sverka_reg, register, post
from datetime import datetime
from terminal.conect import comand
import os



ter = comand()
token_cod = config_read('TOKEN')
bot = TeleBot(token_cod) #Тоукен телеграма
reg_email = {} # Словарь для почты
reg_email.update(sverka_reg()) # Добовление в словарь ранее зарегистрированных пользователей
print(reg_email)
subject_user = {} #Словарь для темы в письме
stop_send = {}
now = datetime.utcnow().strftime('%Y-%m-%d')

@bot.message_handler(commands=['start'], content_types=['text'])
def handler_text(message):  #Главное меню
    user_markup = types.ReplyKeyboardMarkup(True, False)
    user_markup.row(config_read('Button_down_1'))
    user_markup.row(config_read('Button_down_2'))
    bot.send_message(message.from_user.id, config_read('Hello'), reply_markup=user_markup)
    if message.from_user.id not in reg_email:
        bot.send_message(message.chat.id, config_read('Registration'))
        sent = bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(sent, save_link)
    if message.from_user.id not in stop_send.keys():
        add_limit = {message.from_user.id: [now, 0]}
        stop_send.update(add_limit)

@bot.message_handler(commands=['stop'])
def handler_text(message):
    hide_marup = types.ReplyKeyboardMarkup(True, True)
    bot.send_message(message.from_user.id, 'Пока'.encode('utf-8'), reply_markup=hide_marup)

@bot.message_handler(content_types=['text', "photo"])
def read_answer(message): #Основные условия
    pass2 = 0
    if message.text in ['???', 'Автор', 'Help'] and pass2 ==0:
        bot.send_message(message.chat.id, 'Автор и разработчик программы Кириченко Александр Валерьивич по '
                                          'разработано для компании ТОО МФО "КМФ"')
    if message.text in ['Reboot'] and message.from_user.id in admin() and pass2 == 0:
        bot.send_message(message.chat.id, f'Идет перезагрузка')
        os.system('shutdown -r -f -t 0')
        pass2 = 1

    if message.text in ['to', 'To', 'TO', 'tO', 'то', 'ТО', 'То', 'тО']\
            and message.from_user.id in admin() and pass2 == 0:
        sent = bot.send_message(message.chat.id, "Введите номер ТО:")
        bot.register_next_step_handler(sent, to)
        pass2 = 1

    if message.text == config_read('Re_registration') and pass2 == 0:
        sent = bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(sent, save_link)
        pass2 = 1
    if message.text in ['Reboot'] and message.from_user.id in admin() and pass2 == 0:
        bot.send_message(message.chat.id, config_read('Button_down_2'))
        pass2 = 1
    if message.from_user.id in reg_email and pass2 == 0 and message.from_user.id not in subject_user \
            or message.text == config_read('Button_down_2') and pass2 == 0:
        push(message)
    elif message.text == config_read('Button_down_1') and pass2 == 0:
        pusk_answer(message)
    elif message.content_type == 'photo' and message.from_user.id not in reg_email and pass2 == 0:
        sent = bot.send_message(message.chat.id, "По фото я не могу распознать вашь адрес.\nВведите email:")
        bot.register_next_step_handler(sent, save_link)
    else:
        if message.from_user.id not in reg_email.keys() and pass2 == 0:
            bot.send_message(message.chat.id, config_read('Registration'))
            sent = bot.send_message(message.chat.id, "Введите email:")
            bot.register_next_step_handler(sent, save_link)

        else:
            if pass2 == 0:
                pusk_answer(message)

def push(message):
    keyboard = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text=config_read('Button_name_1'), callback_data=config_read('Button_send_1'))
    item2 = types.InlineKeyboardButton(text=config_read('Button_name_2'), callback_data=config_read('Button_send_2'))
    item3 = types.InlineKeyboardButton(text=config_read('Button_name_3'), callback_data=config_read('Button_send_3'))
    item4 = types.InlineKeyboardButton(text=config_read('Button_name_4'), callback_data=config_read('Button_send_4'))
    keyboard.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Выберите тему заявки", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def pusk_answer(message): #Основные условия
    if message.from_user.id not in stop_send.keys():
        add_limit = {message.from_user.id: [now, 0]}
        stop_send.update(add_limit)
    elif stop_send[message.from_user.id][0] != now:
        stop_send[message.from_user.id][1] = 0
        stop_send[message.from_user.id][0] = now
    if message.from_user.id in reg_email.keys():
        if message.from_user.id in subject_user.keys():
            if stop_send[message.from_user.id][1] in [2, 4, 6, 8]:
                push(message)
            if stop_send[message.from_user.id][1] != 10:
                stop_send[message.from_user.id][1] += 1
                if message.text == config_read('Button_down_1'):
                    podskazka(message)
                else: sd(message)
            else:
                bot.send_message(message.chat.id, f"Вы не можете отправить более 10 "
                                                  f"заявок в день через Telegram Bot")

    else:
        bot.send_message(message.chat.id, config_read('Registration'))
        sent = bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(sent, save_link)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def podskazka(message):
    sd_send = bot.send_message(message.chat.id, "Вы может описать проблему и отпраить заявку в СД:")
    bot.register_next_step_handler(sd_send, sd)

@bot.message_handler(func=lambda message: True, content_types=["text", "photo"])
def to(message): #Основные условия
    slov = to_slovar()

    try:
        text = int(message.text)
        save_subject = {message.chat.id: [config_read('Button_send_1'), text]}
        subject_user.update(save_subject)

        if text in slov:
            keyboard = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton(text='TO reboot',
                                                callback_data='reboot_TO')
            item2 = types.InlineKeyboardButton(text='MIE reboot',
                                                callback_data='reboot_mie')
            item3 = types.InlineKeyboardButton(text='Cкриншот',
                                                callback_data='screen')
            item4 = types.InlineKeyboardButton(text='СД заявка',
                                               callback_data='SD_send')
            keyboard.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, "Действия", reply_markup=keyboard)
    except:
        bot.send_message(message.chat.id, 'Введите только № TO')


@bot.message_handler(func=lambda message: True, content_types=["text"])
def save_link(message):   # Регистрация ID и почты в фаил и временый документ
    if message.content_type == 'text':
        my_link = message.text
        if email(message.text):
            add_email = {message.from_user.id: my_link}
            register(f'{message.from_user.id}: {my_link.lower()}')
            reg_email.update(add_email)
            bot.send_message(message.chat.id, f"Сохранил: {my_link} \nНажмите /strat для вызова меню")
        else:
            bot.send_message(message.chat.id, config_read('Incorrect_address'))

@bot.callback_query_handler(func=lambda c: True)
def inline(callback):   # Выбор темы
    if callback.data in [config_read('Button_send_1'), config_read('Button_send_2'), config_read('Button_send_3'),
                         config_read('Button_send_4')]:
        save_subject = {callback.from_user.id: [callback.data, '']}
        subject_user.update(save_subject)

    elif callback.from_user.id in subject_user:
        if subject_user[callback.from_user.id][1] != '':
            to_number = subject_user[callback.from_user.id][1]
            ip = to_slovar()[to_number][1]
            path = f'{ip}.png'
            from_addr = to_slovar()[to_number][2]
            text_send = f"Добрый ден!\n Прошу отремантировать ТО {to_number} {to_slovar()[to_number][0]}\n Дата: {now}"
            if callback.data == 'reboot_mie':
                try:
                    ter.reboot_mie(ip)
                except:
                    bot.send_message(callback.from_user.id, f'Нет соединения с TO №{to_number} по IP: {ip}')
            elif callback.data == 'screen':
                try:
                    ter.screen(ip)
                    photo = open(path, 'rb')
                    bot.send_photo(callback.from_user.id, photo)
                except:
                    bot.send_message(callback.from_user.id, f'Нет соединения с TO №{to_number} по IP: {ip}')
            elif callback.data == 'reboot_TO':
                try:
                    ter.reboot_TO(ip)
                except:
                    bot.send_message(callback.from_user.id, f'Нет соединения с TO №{to_number} по IP: {ip}')
            elif callback.data == 'SD_send':
                try:
                    ter.screen(ip)
                    post(from_addr, config_read('Button_send_1'), text_send, path)
                    bot.send_message(callback.from_user.id, f"Ваша заявка успешно отправлена с адреса: {from_addr}")
                except Exception as err:
                    bot.send_message(callback.from_user.id, f'Не удолось отправить заявку в СД')
                    bot.send_message(callback.from_user.id, f'Ошибка: {err}')



    else:
        save_subject = {callback.from_user.id: [None, '']}
        subject_user.update(save_subject)



@bot.message_handler(func=lambda message: True, content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def sd(message):   # Определение формата сообщения
    from_addr = reg_email[message.from_user.id]
    try:
        if message.content_type == 'photo':
            text_photo = message.caption
            id_photo = message.photo[2].file_id
            file_info = bot.get_file(id_photo)
            print(f"http://api.telegram.org/file/bot{token_cod}/{file_info.file_path}")  # Выводим ссылку на файл

            if text_photo is None:
                bot.send_message(message.chat.id, f"Фото должно содержать комментарий об ошибке, без комментария "
                                                  f"к фото содержащих описание проблемы заявка не будет отправлена.")
            else:
                subject = subject_user[message.from_user.id][0]
                path = f"http://api.telegram.org/file/bot{token_cod}/{file_info.file_path}"
                post(from_addr, subject, text_photo, path)
                bot.send_message(message.chat.id, f"Ваша заявка успешно отправлена с адреса: {from_addr}")
        elif message.content_type == 'text' and message.text != config_read('Button_down_1') and message.text != \
                config_read('Button_down_2'):
            subject = subject_user[message.from_user.id][0]
            path = None
            body_text = message.text
            post(from_addr, subject, body_text, path)
            bot.send_message(message.chat.id, f"Ваша заявка успешно отправлена с адреса: {from_addr}")
        else:
            bot.send_message(message.chat.id, f"Данный формат заявки не допустим или не коректно описали тему")
    except Exception as err:
        bot.send_message(message.chat.id, f'Не удолось отправить заявку в СД')
        bot.send_message(message.chat.id, f'Ошибка: {err}')




bot.polling(none_stop=True)