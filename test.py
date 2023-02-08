import telebot

bot = telebot.TeleBot('5837573924:AAEHV5f2IHO995x8FU4t3u_MTqIFZRgW9fM'); 

def MessageToCouple(couple, mes):
    for ids in couple:
        bot.send_message(ids, mes) 

def CheckMessage(string):
    correctString = string
    wasFound = False
    for i in string.split(" "):
        for j in badWords:
            if i.lower() == j:
                wasFound = True
                correctString = correctString.replace(i, "*" * len(i))
    return [correctString, wasFound]

def AddCouple():
    temp = [inSearch.pop(0), inSearch.pop(0)]
    couples.append(temp)
    MessageToCouple(temp, "Собеседник найден! Чтобы прекратить диалог, пропишите /end")

def EndDialogue(id):
    for i in range(len(couples)):
        if id in couples[i]:
            MessageToCouple(couples[i], "Диалог завершён. Пропишите /find , чтобы найти нового собеседника")
            couples.remove(couples[i])
            return

@bot.message_handler(content_types=["photo"])
def photo(message):
    for ids in couples:
        if (message.from_user.id in ids):
            for i in ids:
                if i != message.from_user.id:
                    idphoto = message.photo[0].file_id
                    bot.send_photo(i, idphoto )
                    return
    bot.send_message(message.from_user.id, f"У вас не имеется партнера, чтобы передать это сообщение.")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if str(message.text).lower() == "/help": 
        bot.send_message(message.from_user.id, "/find - начинает поиск собеседника, /stop - прекращает поиск собеседника, /end - заканчивает диалог с собеседником")
    elif str(message.text).lower() == "/start":
        bot.send_message(message.from_user.id, "Здравствуй! Чтобы получить возможный список команд - пропиши /help")
    elif str(message.text).lower() == "/find":
        for i in couples:
            if message.from_user.id in i:
                bot.send_message(message.from_user.id, "У вас уже есть собеседник.")
                return
        if message.from_user.id not in inSearch:
            bot.send_message(message.from_user.id, "Подбор начат. Остановить подбор - /stop")
            inSearch.append(message.from_user.id)
            if (len(inSearch) >= 2):
                AddCouple()
        else:
            bot.send_message(message.from_user.id, "Вы уже начали поиск, пожалуйста, подождите...")
    elif str(message.text).lower() == "/stop":
        if message.from_user.id in inSearch:
            inSearch.remove(message.from_user.id)
            bot.send_message(message.from_user.id, "Вы больше не ищите собеседника.")
        else:
            bot.send_message(message.from_user.id, "Для начала пропишите команду /find")
    elif str(message.text).lower() == "/end":
        EndDialogue(message.from_user.id)
    else:
        for ids in couples:
            if (message.from_user.id in ids):
                for i in ids:
                    if i != message.from_user.id:
                        result = CheckMessage(message.text)
                        correctMessage = result[0]
                        bot.send_message(i, correctMessage)
                        if result[1]:
                            EndDialogue(message.from_user.id)
                        return
        bot.send_message(message.from_user.id, f"У вас не имеется партнера, чтобы передать это сообщение.")

badWords = ["лс", "личку", "ls"]
inSearch = []
couples = []
bot.polling(none_stop=True, interval=0)