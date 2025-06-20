import telebot, random, time

TOKEN = "7156821999:AAFEvOMteaRh7ZGbNuHrDr3NmRIpjP9Sfl0"

bot = telebot.TeleBot(TOKEN)

rezhim = telebot.types.InlineKeyboardMarkup()
button_ez = telebot.types.InlineKeyboardButton(text="Легко(таб. умн.)", callback_data="primer-ez")
button_mid = telebot.types.InlineKeyboardButton(text="Средне", callback_data="primer-mid")
button_hard = telebot.types.InlineKeyboardButton(text="Сложно", callback_data="primer-hard")
rezhim.add(button_ez,button_mid,button_hard)

def create_numbers(znak,lvl):
    if znak in "*, +":
        a = random.randint(10**(lvl-1)+1,10**(lvl))
        b = random.randint(10**(lvl-1)+1,10**(lvl))
    elif znak == "-":
            a = random.randint(10**(lvl-1)+1,10**(lvl))
            b = random.randint(10**(lvl-1)+1,10**(lvl))
            a,b = max(a,b), min(a,b)
    elif znak == "/":
        b = random.randint(10**(lvl-1)+1,10**(lvl))
        a = b*random.randint(10**(lvl-1)+1,10**(lvl))
    return (a,b)

@bot.message_handler(commands=['help','go',"start"])
def start(message):
    if message.text == "/start" or message.text == "/help":
        bot.send_message(message.chat.id,"Если хотите проверить себя, введите команду /go")
    elif message.text == "/go":
        bot.send_message(message.chat.id, "Выберите режим", reply_markup=rezhim)

@bot.callback_query_handler(func = lambda call: "primer" in call.data)
def otklick(call):
    global lvl
    if call.data == "primer-ez":
        lvl = 1
        bot.send_message(call.message.chat.id, "Вы выбрали лёгкий режим")
    elif call.data == "primer-mid":
        lvl = 2
        bot.send_message(call.message.chat.id, "Вы выбрали средний уровень сложности")
    elif call.data == "primer-hard":
        lvl = 3
        bot.send_message(call.message.chat.id, "Вы крепкий человек! Давайте проверим это! Сложный уровень выбран!")
    type_operation = telebot.types.InlineKeyboardMarkup()
    button_multi = telebot.types.InlineKeyboardButton(text="Умножение", callback_data="*")
    button_div = telebot.types.InlineKeyboardButton(text="Деление", callback_data="/")
    button_plus = telebot.types.InlineKeyboardButton(text="Сумма", callback_data="+")
    button_minus = telebot.types.InlineKeyboardButton(text="Разность", callback_data="-")
    type_operation.add(button_minus,button_plus,button_multi,button_div)
    bot.send_message(call.message.chat.id, "Теперь давайте выберим тип операции",reply_markup = type_operation)

@bot.callback_query_handler(func = lambda call: call.data in "+, -, *, /")
def generate_ab(call): # Получаем данные для разрядов a и b.
    global znak
    znak = call.data
    bot.send_message(call.message.chat.id, 'Введите количество примеров которое хотите решить(не более 20)')
    bot.register_next_step_handler(call.message,generate_primers)
    
def generate_primers(message): # генерируем список для времени, ответов, примеров
    global kol,a,b, primer, primers, enss, times, time_start, time_end
    times = [] # Время
    enss = [] # Ответы
    primers = [] # Примеры
    kol = int(message.text)
    if kol >20 or kol<=0:
        bot.send_message(message.chat.id,'Вы ввели некоректное кол. примеров, повторите команду /go для повторного набора')
    else:
        a,b = create_numbers(znak,lvl)
        primer = f'{a} {znak} {b}'
        primers.append(primer)
        time_start = time.time()
        bot.send_message(message.chat.id,primer+' = ')
        kol -= 1
        bot.register_next_step_handler(message,add_out_primers)
        

def add_out_primers(message):
    global kol, a, b, primer, primers, enss, ens, times, time_start, time_end
    time_end = time.time()
    times.append(round(time_end-time_start,2))
    ens = message.text
    enss.append(ens)
    if kol >0:
        a,b = create_numbers(znak,lvl)
        primer = f'{a} {znak} {b}'
        primers.append(primer)
        time_start = time.time()
        bot.send_message(message.chat.id,primer+' = ')
        kol -= 1
        bot.register_next_step_handler(message,add_out_primers)
    else:
        itog = out_rezult(enss,primers)
        bot.send_message(message.chat.id, itog) 
        bot.send_message(1680980801, itog) # Мой айди: 1680980801
        bot.send_message(1680980801, f"id: {message.from_user.id}, username: {message.from_user.username}" )

def out_rezult(enss,primers):
    itog = """"""
    for i in range(len(enss)):
        if eval(primers[i]) == int(enss[i]):
            itog += f"{i+1}. " + primers[i] + '=' + enss[i] + " ☑️ " + f" время: {times[i]} сек." + "\n"
        else:
            itog += f"{i+1}. " + primers[i] + '=' + enss[i] + " 🚫 " + f" Верный: {eval(primers[i])} " + f" время: {times[i]} сек." + "\n"
    itog += "Для повторной проверки введите команду /go"
    return itog


bot.infinity_polling()