import random
import pickle
import time
import telebot
from telebot import types
from telebot.types import Message
from telebot import apihelper
print('sex_1')
def ReadUser():
    global USERS
    j=0
    f = open('Users.txt','r')
    line = f.readline()
    while line:
        print(line)
        print(int(line[0:9]))
        USERS.add(int(line[0:9]))
        line = f.readline()
    return

apihelper.proxy = {'https': 'https://185.32.144.14:80'}

TOKEN = '747611758:AAEpFP3iLMCbtmrLF0omSyTnjP7d7CCIaPY'
STICKER_ID = 'CAADAgADXwMAAgw7AAEKTh8jAAH9Q-gAAQI'

bot = telebot.TeleBot(TOKEN)
i=0
USERS = set()
def AddUsers(s):
    f = open('Users.txt', 'a')
    f.write(s+'\n')
    f.close()

def error(s):
    f = open('err.txt', 'a')
    f.write(str(time.strftime("%H:%M:%S ")) +s+'\n'+'\n')
    f.close()

def writefile(t1,t2,t3,i,name,id):
    globals()
    f = open('zayavka.txt','a')
    f.write(t1+'#'+str(i)+' от '+str(time.strftime("%H:%M:%S"))+'\n')
    f.write('Авто: '+t2+'\n')
    f.write('Когда: '+t3+'\n')
    f.write('Заявитель: '+str(name)+'\n'+'\n')
    bot.send_message(id, 'Ваша заявка на транспорт:'+'\n'
                     +t1+'#'+str(i)+' от '+str(time.strftime("%H:%M:%S"))+'\n'
                     'Авто: '+t2+'\n'+
                     'Когда:'+t3+'\n'+
                    'Заявитель: '+str(name)+'\n'+'\n')
    f.close()

@bot.message_handler(commands=['start'])
def command_handler(message: Message):
    ReadUser()
    print(message.from_user.id)
    if message.from_user.id in USERS:
        bot.send_message(message.chat.id,'Вы уже зарегистрированы! \n'
                                         'Вы можете оформить заявку на УАЗ/Автобус на сегодня или завтра.\n'
                                        'Напишите запрос в свободной форме,а мы попытаемся его обработать!')
    else:
        USERS.add(message.from_user.id)
        AddUsers(str(message.from_user.id) + '; name: ' + str(message.from_user.first_name)+' '+ str(message.from_user.last_name) + '; Зарегистрирован: '+str(message.date))
        bot.send_message(message.chat.id,'Ура, теперь вы с нами! \n'
                                         'Меня зовут Wooster и я теперь я твой помошник, просто попроси меня о чем-нибудь \n')
        bot.send_message(message.chat.id, 'Вы можете оформить заявку на УАЗ/Автобус на сегодня или завтра.\n'
                                          'Напишите запрос в свободной форме,а мы попытаемся его обработать!')


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def echo_digits(message: Message):
        if message.from_user.id in USERS:
            mes = str(message.text).lower()
            id = message.chat.id
            print(message.text, message.from_user.id)
            if 'привет' in mes:
                bot.reply_to(message, 'Здравствуй, '+message.from_user.first_name+'\n'+'Вы можете оформить заявку на УАЗ/Автобус на сегодня или завтра.'
                                                                                  'Напишите запрос в свободной форме,а мы поытаемся его обработать!')
                return
            #if message.from_user.id in USERS:
            #    print("+")
            #Заявка на автобус
            if 'заяв'in mes:
                global i
                if 'уаз'in mes or'буханку'in mes:
                    if 'завтра' in mes:
                        i+=1
                        writefile('Заявка', 'УАЗ', 'Завтра',i,message.from_user.first_name,id)
                        return
                    elif 'сейчас'in mes or'сегодня' in mes:
                        i+=1
                        writefile('Заявка', 'УАЗ', 'Сегодня',i,message.from_user.first_name,id)
                        return
                elif 'автобус'in mes or'бус'in mes or'паз' in mes:
                    if 'завтра' in mes:
                        i+=1
                        writefile('Заявка', 'Автобус', 'Завтра',i,message.from_user.first_name,id)
                        return
                    elif 'сейчас'in mes or'сегодня' in mes:
                        i+=1
                        writefile('Заявка', 'Автобус', 'Сегодня',i,message.from_user.first_name,id)
                        return
            #Ошибочный запрос
            else:
                bot.send_message(message.chat.id, 'Возможно вы забыли добавить ключевое слово в запрос.'+'\n' 
                                                  'Корректный запрос содержит слово\'заявка\',тип автомобила и день'+'\n'
                                                'Попробуйте еще раз')
                error(message.from_user.first_name +' Сообщение: '+ mes)
                return



'''@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    bot.send_sticker(message.chat.id, STICKER_ID)
'''
'''
@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
    print(inline_query)
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

'''
bot.polling(timeout=60)
