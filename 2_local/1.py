import telebot

token = '7342084415:AAH67x-rKBOvJkRzy0nt1zIASd0UAutrJrs'
bot = telebot.TeleBot(token, threaded=False)


@bot.message_handler(content_types=["text"])
def start(message):
    if message.text == "/start":
        kb = telebot.types.InlineKeyboardMarkup()
        key = telebot.types.InlineKeyboardButton(text="Регистрация", callback_data="registrations")
        kb.add(key)

        key = telebot.types.InlineKeyboardButton(text="Расписание", callback_data="shedule")
        kb.add(key)

        text = "Привет! У я буду рассылать вам актуальную информацию. Ваш выбор:"
        bot.send_message(message.from_user.id, text, reply_markup=kb)
    else:
        print('Я хотел команду старт, но ты написал что-то другое')


@bot.callback_query_handler(func=lambda call: True)
def callback_start(call):
    if call.from_user.is_bot:
        return

    print(f'Пользователь выбрал {call.data}')

    if call.data == "shedule":
        chat_id = call.message.chat.id
        message = get_shedule(chat_id)
        kb = telebot.types.InlineKeyboardMarkup()
        key = telebot.types.InlineKeyboardButton(text="Меню", callback_data="menu")
        kb.add(key)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.id,
            text=message,
            parse_mode='HTML',
            reply_markup=kb,
        )
        text = 'Получи и распишись!'
        bot.send_message(chat_id, text, reply_markup=kb)

    elif call.data == 'registrations':
        pass
    elif call.data == 'menu':
        pass


def get_shedule(user_id):
    role_dct = {
        'pdo': ['1702642815'],
    }

    user_role = None
    for k, v in role_dct.items():
        if str(user_id) in v:
            user_role = k
            break
    if user_role is None:
        return

    with open('shedule.txt') as f:
        fr = f.readlines()

    shedule_lst = list()
    for word in fr:
        word = word.strip()
        predmet, user, role = word.split('|')
        shedule_lst.append({
            'user': user,
            'role': role,
            'predmet': predmet,
        })
    
    ret = list()
    for shedule in shedule_lst: 
        if user_role in shedule['role']:
            ret.append(shedule['predmet'])
    message = '\n'.join(ret)
    return message


if __name__ == '__main__':
    # get_shedule(1702642815)
    bot.polling(none_stop=True)