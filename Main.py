
import time
import telebot
from telebot.types import Message
import os
import psycopg2

DATABASE_URL = os.environ['postgres://lmujffhuwvdwlq:b5831431d3051c1d92186990331a34506481c652cf5fd52f0c56aad5a12b87b6@ec2-46-137-113-157.eu-west-1.compute.amazonaws.com:5432/d43638j1mqjsms']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def ReadUser():
    global USERS
    f = open('Users.txt','r')
    line = f.readline()
    while line:
        USERS.add(int(line[0:9]))
        line = f.readline()
    return

TOKEN = '747611758:AAEpFP3iLMCbtmrLF0omSyTnjP7d7CCIaPY'
STICKER_ID = 'CAADAgADXwMAAgw7AAEKTh8jAAH9Q-gAAQI'

bot = telebot.TeleBot(TOKEN)
i=0

bot.send_message(260119686,'я жив')
bot.send_photo(260119686, 'files/1.jpg')

USERS = set()

def AddUsers(s):
    f = open('Users.txt', 'a')
    f.write(str(s)+'\n')
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
    print(message.from_user.id)
    if message.from_user.id in USERS:
        bot.send_message(message.chat.id,'Вы уже зарегистрированы! \n'
                                         'Вы можете оформить заявку на УАЗ/Автобус на сегодня или завтра.\n'
                                        'Напишите запрос в свободной форме,а мы попытаемся его обработать!')
    else:
        print(str(message.from_user.id)+'ne naideno') #
        ReadUser()
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

bot.polling(timeout=60)
