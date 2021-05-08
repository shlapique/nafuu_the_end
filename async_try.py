# Это будет попыткой сделать одновременное получение пикч для нескольких пользователей
# тут, очев, не нужен метод userplace_counter, потому что делать будем все одновременно 

import telebot;
import time; #это нам надо для точного времени обновления
import requests; 
import os; # это надо для того, чтобы мы могли удалить старый файл html
import subprocess # это я делаю, что бы вызвать parser.exe
from requests import request # это нам надо для скачивания html страницы

# тут глобальная переменная, которая будет уведомлять, что пользователь нажал /start
# мы его проверили на наличие в базе пользователей, которые уже активировали чат
startFlag = 0

# глобальная переменная для остановки отправки контента
# это начальное значение аборта
abort = 0

# Указываем токен
token = "1625904665:AAH7lA2qrv-tKvNfsB1iq_MrSy7OabgLR74"
bot = telebot.AsyncTeleBot(token)

dir_path = os.path.join('C:\\', 'Nafuu_parser_bot')

# точный путь файла для записи линков
#myfilelinks = 'C:/Users/Fantom/source/repos/parser ver 1.1/parser ver 1.1/temp_links.txt'

# путь до файла с общим логом
logpath = 'C:/Users/Fantom/source/repos/parser ver 1.1/parser ver 1.1/Log.txt'

# основная директория, которой мы будем приписывать названия тредов
maindir = dir_path +'\\botUsers\\'

# путь к списку пользователей
userspath = dir_path +'\\botUsers\\botUsers.txt'

# путь к файлу очереди, где записаны пользователи
queuepath = dir_path +'\\queue.txt'

# bant, c, e, p, toy, vip, vp, vt, w, wg, wsr
bant = '\\bant.txt'
c = '\\c.txt'
e = '\\e.txt'
out = '\\out.txt'
p = '\\p.txt'
toy = '\\toy.txt'
vip = '\\vip.txt' 
vp = '\\vp.txt'
vt = '\\vt.txt'
w = '\\w.txt'
wg = '\\wg.txt'
wsr = '\\wsr.txt'

# в последних версиях проекта эта функция стала попусту ненужна,
# но пусть здесь просто будет, не хочу ее убирать
def userplace_counter(message):
    a = 0
    line = '5454'
    f = open(queuepath,"r")
    while line:    
        line = f.readline()
        a += 1
    f.close() 
    return a

# в целом функция проверяет наличие пользователя в общем потоке
# то есть получает он какие-либо обновления или нет
# если да, то мы его шлем далеко
def impatient(message):
    # преобразовываем значение id из int в string
    userid = str(message.chat.id)
    
    line = '5454'
    f = open(queuepath,"r")
    while line:
        line = f.readline();
        if(line == ''):
            break
        # тут мы удаляем \n, чтобы не было ошибки при отправке
        line = line.strip('\n')
        if (line == userid):
            bot.send_message(message.chat.id, "Jeeeez... u touched this shi again... Жди, пожалуйста, я же тебе сейчас и так уже отправляю пикчи!")
            bot.send_message(message.chat.id, "Если ты хочешь закончить процесс, пришли /abort.")
            return 0
    f.close()

# это функция будет проверять наличие пользователя в списке приглашенных
# мб, это функция будет не нужна, но пока что пусть будет
def check_invitelist(message):
    # преобразовываем значение id из int в string
    userid = str(message.chat.id)
    f = open(userspath, 'r');
    line = '5454'
    # тут сделаем флаг, чтобы понять, нашли ли мы id пользователя в списке или нет
    flag = 0
    while line:
        line = f.readline();
        if(line == ''):
            break
        # тут мы удаляем \n, чтобы не было ошибки при отправке
        line = line.strip('\n')
        if (line == userid):
            print ("Пользователь " + userid + " есть в списке приглашенных, все ОК")
            flag = 1
    f.close()
    if (flag == 0):
        print("Пользователя " + userid + " НЕТ в списке приглашенных... Он пытается получить доступ к боту!")
        bot.send_message(message.chat.id, "Тебя НЕТ в списке приглашенных! Вот твой id: " + userid)
        bot.send_message(message.chat.id, "Если хочешь получить доступ к боту, тебе надо сообщить твой id администратору.")
        return 0

# за бессмысленное повторение кода можно получить в рыльце, поэтому...(((
def cmd_func(message, thread):
    # тут мы делаем защиту, чтобы незванный гость не смог использовать бота
    a = 1
    a = check_invitelist(message)
    if (a == 0):
        return 1    
    # проверяем, нажимал ли чел уже эту кнопку или нет
    # флаг на проверку дурака
    foolflag = 1
    # если он у нас есть в списке, то он его хейтит
    foolflag = impatient(message)
    if (foolflag == 0):
        return 2
        
    print("Пользователь нажал /" + thread + " ...")
    bot.send_message(message.chat.id, 'Обновление займет некоторое время... wait pls☺')
    print("Пользователь нажал апдейт...")
    source = ("https://archive.nyafuu.org/" + thread + "/")
    update_nafuu(message, source, thread)    

# функция, которая будет проверять, есть ли папка на пользователя или нет
def check_user_data(message):
    # это путь к папке с файлами на пользователя
    # преобразовываем значение id из int в string
    userid = str(message.chat.id)
    user_path = maindir + userid # пример:'C:/Users/Fantom/source/repos/parser ver 1.1/parser ver 1.1/botUsers/771330279'
   
    '''
    #проверка на наличие пользователя в базе
    
    '''
    if os.path.isdir(user_path): # НЕ ПУТАТЬ C os.path.isfile!!!!!
        bot.send_message(message.chat.id, "Ты уже пользовался мной... вот твой id = " + userid)
        print ("Пользователь " + userid + " уже есть в базе...")
    else:
        # если пользователя нет, заводим папку на пользователя
        os.mkdir(user_path)
        # далее создаем лог на пользователя
        f = open(user_path + '/LOG.txt', 'w')
        f.close()
        # создаем файлы под все треды
        f = open(user_path + bant, 'w')
        f.close()
        f = open(user_path + c, 'w')
        f.close()
        f = open(user_path + e, 'w')
        f.close()
        f = open(user_path + out, 'w')
        f.close()
        f = open(user_path + p, 'w')
        f.close()
        f = open(user_path + toy, 'w')
        f.close()
        f = open(user_path + vip, 'w')
        f.close()
        f = open(user_path + vp, 'w')
        f.close()
        f = open(user_path + vt, 'w')
        f.close()
        f = open(user_path + w, 'w')
        f.close()
        f = open(user_path + wg, 'w')
        f.close()
        f = open(user_path + wsr, 'w')
        f.close()
        print("Этого пользователя не было в базе... создал все папки и файлы")


# функция, которая будет создавать файл аборт тхт в
# директории пользователя, чтобы не произошел сбой блин (
def abort(message):
    userid = str(message.chat.id)
    # тут мы создаем путь пользователя
    user_path = maindir + userid # 'C:/Users/Fantom/source/repos/parser ver 1.1/parser ver 1.1/botUsers/771330279'
    abort_path = user_path + "\\ABORT.txt"
    f = open(abort_path, 'w')
    f.close()


# ОСНОВНАЯ ФУНКЦИЯ
def update_nafuu(message, source, thread):
    # тут мы делаем защиту, чтобы незванный гость не смог использовать бота
    a = 1
    a = check_invitelist(message)
    if (a == 0):
        return 1
    
    # флаг на проверку дурака
    foolflag = 1
    # если он у нас есть в списке, то он его хейтит
    foolflag = impatient(message)
    if (foolflag == 0):
        return 2
    
    # преобразовываем значение id из int в string
    userid = str(message.chat.id)
    
    # записываю пользователя в очередь
    # для этого мы открывает файл очереди на запись в конец
    # и дозаписываем туда пользователя
    qfile = open(queuepath, "a")
    qfile.write(userid + "\n")
    qfile.close()
    
    # тут мы создаем путь пользователя, где хранятся треды, логи и тмплинкс
    user_path = maindir + userid # 'C:/Users/Fantom/source/repos/parser ver 1.1/parser ver 1.1/botUsers/771330279'

    # просто локальный путь к файлу реди тхт
    readytxt  = user_path + '\\READY.txt' #'C:/Users/Fantom/source/repos/parser ver 1.1/parser ver 1.1/botUsers/771330279'

    # путь для временного хранения пикчи
    tmppath = user_path +'\\temppic.png'
    
    print("Начинаю обновление...")
    
    # создаем файл реди тхт
    abort_path = user_path + "\\ABORT.txt"
    print("Проверка на наличие файла ABORT...")
    # дефайним, что пользователь еще не нажал аборот
    if os.path.isfile(abort_path):
        os.remove(abort_path)
    print("Файла ABORT нет!...")
    
    # это то, откуда мы будем брать ссылки для конечной отправки 
    myfilelinks = user_path + "\\tmplinks.txt"
    
    # он не стартанул парсер
     # ТУТ ЩА НАВАЛИВАЮ ПРОСТО ГРЯЗЬ
    # СКАЧИВАЮ 3 РАЗА РАЗНЫЕ СТРАНИЦЫ С САЙТА
    # 3 ФАЙЛА ЗАПИСЫВАЮ РАЗНЫМИ ИМЕНАМИ
    # а в парсере мы 3 раза пробегаемся по циклу)
    
    # ссылки на страницы (просто пажилой позор)
    sauce1 = source
    sauce2 = source + 'page/2/'
    sauce3 = source + 'page/3/'
    
    # путь к файлу 1
    myfile1 = user_path + '\\parsetext1.html'
    # путь к файлу 2
    myfile2 = user_path + '\\parsetext2.html'
    # путь к файлу 3
    myfile3 = user_path + '\\parsetext3.html'
    
    print("Удаляю файл со старыми тмп и старые файлы хтмл...")        
    
    if os.path.isfile(myfilelinks):
        os.remove(myfilelinks)
        
    # если существует файл (html), если да, то его удаляет
    if os.path.isfile(myfile1):
        os.remove(myfile1)
    
    # если существует файл (html), если да, то его удаляет
    if os.path.isfile(myfile2):
        os.remove(myfile2)
        
    # если существует файл (html), если да, то его удаляет
    if os.path.isfile(myfile3):
        os.remove(myfile3)
    
    print("Скачиваю новые страницы...")
        
    try:
        # скачиваем html страницу
        t = request('GET', sauce1).text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Ошибка в подключении... ")
        raise SystemExit(e)
    
    # создаем, (если не можем открыть), файл и записываем туда html
    with open(myfile1, 'w', encoding='utf-8') as f:
        f.write(t)
        
    try:
        # скачиваем html страницу
        t = request('GET', sauce2).text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Ошибка в подключении... ")
        raise SystemExit(e)

    # создаем, (если не можем открыть), файл и записываем туда html
    with open(myfile2, 'w', encoding='utf-8') as f:
        f.write(t)
        
    try:
        # скачиваем html страницу
        t = request('GET', sauce3).text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Ошибка в подключении... ")
        raise SystemExit(e)

    # создаем, (если не можем открыть), файл и записываем туда html
    with open(myfile3, 'w', encoding='utf-8') as f:
        f.write(t)
        
    # На выходе получаем 3 файла для парса
    
    print("Скачал html страницы. ")
    
    # по нашей анальной задумке дописываем @ в конец
    # это надо, чтобы парсер знал, когда остановиться 
    with open(myfile1, 'a', encoding='utf-8') as f:
        f.write('@')
    with open(myfile2, 'a', encoding='utf-8') as f:
        f.write('@')
    with open(myfile3, 'a', encoding='utf-8') as f:
        f.write('@')
    
    print('Начинаю сон на 2 секунды...')
    # Сон на 2 секунды
    time.sleep(2)
    
    # после этого происходит парсинг
    ########################
    ########################
    ########################
    
    # ТУТ МЫ ВЫЗЫВАЕМ EXE ОТ ДВУХ ПАРАМЕТРОВ ID + ThREAD
    ########################
    ########################
    ######################## 
    # эта дура (цмд то есть) ваще не могет в пробелы на путях, поэтому надо як проггеры писать с _
    # НАДО БУДЕТ ЩА ДОПИСАТЬ!
    try: 
         subprocess.check_call([dir_path + '\\PARSER_ZUSAMMEN_TEST\\Release\\zusammen_user_test.exe', userid, thread])
    except subprocess.CalledProcessError:
        print("Тут обкакался парсер блинб!")
        
    print('Жду парсер...')
    # ждем удаление файла реди тхт
    while os.path.isfile(readytxt):
        time.sleep(1)    

    # если не существует файла костыля, то все ОК    
    if not os.path.isfile(readytxt):
        print('Все ОК, костыля нет!')
   
    # Сон на 1 секунду
    print('Сплю еще секундочку...')
    time.sleep(1)
    
    ######ОСНОВНОЕ ДЕЙСТВИЕ######
    # ЕСЛИ РАЗМЕР ПИКА >= 10МБ, ТО
    # ТО ВСЕ КРАШИТСЯ
    # ПОТОМУ ЧТО БОТ БОЛЬШЕ НЕ МОЖЕТ ОТПРАВИТЬ
    
    linkf = open(myfilelinks, "r")
    # Пока есть строки, делаем:
    line = '5454'
    # Устанавливаем курсор на начало файла
    #linkf.seek(0)
    while line:
        if os.path.isfile(abort_path):
                bot.send_message(message.chat.id, 'Ты написал ABORT ...=> Завершаю обновления....')
                time.sleep(1)
                break
        # Прочитать строку
        line = linkf.readline()
        #ТУТ НАДО СДЕЛАТЬ ПРОВЕРКУ НА КОНЕЦ файла сразу
        if(line == ''):
            break
        # тут мы удаляем \n, чтобы не было ошибки при отправке
        line = line.strip('\n')
        # ОПЯТЬ КОСТЫЛЬ НА ПРОВЕРКУ РАЗМЕРА ФАЙЛА
        # Сначала скачиваем пик, потом его будем удалять☺
        # скачали пик
        r = requests.get(line)
        
        # тут пытался написать обработчик ошибки 400 
        # получилось так себе (
        #if r.getcode() == 400:
        #    print("ОШИБКА 400... не могу скачать ссылку... пропускаю пикчу...")
        #    continue
        # записали его в файл
        with open(tmppath, 'wb') as f: 
            f.write(r.content)
        info = os.stat(tmppath)
        #сравнили размер файла в байтах с макс размером пика
        print(info.st_size)
        if info.st_size >= 5242880:
            print(line)
            print(info.st_size)
            print("Размер файла привышает максимальный для отправки!")
            # удаляем файл
            os.remove(tmppath)
            continue
        # удаляем файл
        os.remove(tmppath)
        # тут мы узнаем расширение (тип) файла (png, jpg - как фото, а gif - как видео)
        # пикаем ласт 3 символа из строки
        type = line[-3:]
        # если гиф, то:
        if (type == 'gif'):
            print(line)
            print("Это гифа!")
            if os.path.isfile(abort_path):
                bot.send_message(message.chat.id, 'Ты написал ABORT ...=> Завершаю обновления....')
                time.sleep(1)
                break
            #Присылаем гиф пользователю
            # ловим исключения апи
            try:
                bot.send_video(message.chat.id, line, None, 'gif')
            except Exception as e:
                print(e)
                print("Попалось исключение, поэтому мы его скипаем...")
                continue
            # Проверяем, нажал ли пользователь /abort
            if os.path.isfile(abort_path):
                bot.send_message(message.chat.id, 'Ты написал ABORT ...=> Завершаю обновления....')
                time.sleep(1)
                break
            
        elif (type == 'ebm'): # Это значит, что я присылаю вебм
              print(line)
              print("Это webm!")
              print("Скипаю...")
              continue

        else:
            print(line)
            if os.path.isfile(abort_path):
                bot.send_message(message.chat.id, 'Ты написал ABORT ...=> Завершаю обновления....')
                time.sleep(1)
                break
            
            #Присылаем пик пользователю
             # ловим исключения апи
            try:
                bot.send_photo(message.chat.id, line)
            except Exception as e:
                print(e)
                print("Попалось исключение, поэтому мы его скипаем...")
                continue
            # Сон на 1 секунду
            time.sleep(1)
            if os.path.isfile(abort_path):
                bot.send_message(message.chat.id, 'Ты написал ABORT ...=> Завершаю обновления....')
                time.sleep(1)
                break
            
    # удаляем темп тхт
    # Закрываем указатель на этот файл
    linkf.close()
    #if os.path.isfile(myfilelinks):
    #    os.remove(myfilelinks)
    #os.remove(myfilelinks)
    time.sleep(5)
    bot.send_message(message.chat.id, 'Пока это все, что есть 🤗')
    print("рассчет окончен!")
    print("Удаляю пользователя из очереди...")
    # откываю файл с очередью
    f = open(queuepath,"r")
    # читаю все строки
    lines = f.readlines()
    f.close()
    f = open(queuepath,"w")
    for line in lines:
        # если нашли ид, то записываем в файл все, кроме него
        if line!= userid +"\n":
            f.write(line)
    f.close()
    
    print("Удаляю файл ABORT...")
    if os.path.isfile(abort_path):
        os.remove(abort_path)
    else:
        print("Файла ABORT не обнаружил!")
        
        
# Метод под команду /start
@bot.message_handler(commands=['start'])
def start_message(message):
    a = 1
    a = check_invitelist(message)
    if (a == 0):
        return 1
    check_user_data(message)
    print(message)
    print(message.chat.id)
    global startFlag
    if (startFlag == 0):
        bot.send_message(message.chat.id, 'Ты написал мне "start". Так давай начнем!😒')
        bot.send_message(message.chat.id, 'Напиши мне "/help", чтобы узнать, что я умею🧠')
        # Сон на 1 секунду
        time.sleep(1)
        bot.send_message(message.chat.id, 'Если хочешь закончить программу, то пришли /abort (Это пока что в бета-тестировании...)')
        startFlag = 1
    else:
        print("Пользователь нажал /start, хотя уже был в базе.")

@bot.message_handler(commands=['help'])
def help_message(message):
    # тут мы делаем защиту, чтобы незванный гость не смог использовать бота
    a = 1
    a = check_invitelist(message)
    if (a == 0):
        return 1
    
    print(message)
    print(message.chat.id)
    bot.send_message(message.chat.id, '/bant - International/Random🔞 **(worst place on earth)\n/c - Anime/Cute **(sometimes mature content)\n/e - Ecchi🔞\n/out - Outdoors\n/p - Photography\n/toy - Toys\n/vip - Very Impotent Posers\n/vp - Pokémon\n/vt - Virtual YouTubers\n/w - Anime/Wallpapers **(mpbile-pc)\n/wg - Wallpapers/General **(mpbile-pc)\n/wsr - Worksafe Requests')

'''
@bot.message_handler(commands=['abort'])
def abort_command(message):
    # тут мы делаем защиту, чтобы незванный гость не смог использовать бота
    a = 1
    a = check_invitelist(message)
    if (a == 0):
        return 1
    
    print('Пользователь завершил программу')
    print("Заврешаю цикл...")
    # СОЗДАЕМ КОСТЫЛБ ... ДА, опять.. (
    # при вызове аборта мы создаем файл ABORT.TXT
    abort(message)
'''
@bot.message_handler(commands=['bant'])
def update_bant(message):
    thread = "bant" # название треда
    cmd_func(message, thread)
    
@bot.message_handler(commands=['c'])
def update_c(message):
    thread = "c" # название треда
    cmd_func(message, thread)    

@bot.message_handler(commands=['e'])
def update_e(message):
    thread = "e" # название треда
    cmd_func(message, thread)
    
@bot.message_handler(commands=['out'])
def update_out(message):
    thread = "out" # название треда
    cmd_func(message, thread)
    
@bot.message_handler(commands=['p'])
def update_p(message):
    thread = "p" # название треда
    cmd_func(message, thread)
    
@bot.message_handler(commands=['toy'])
def update_toy(message):
    thread = "toy" # название треда
    cmd_func(message, thread)

@bot.message_handler(commands=['vip'])
def update_vip(message):
    thread = "vip" # название треда
    cmd_func(message, thread)

@bot.message_handler(commands=['vp'])
def update_vp(message):
    thread = "vp" # название треда
    cmd_func(message, thread)
    
@bot.message_handler(commands=['vt'])
def update_vt(message):
    thread = "vt" # название треда
    cmd_func(message, thread)

@bot.message_handler(commands=['w'])
def update_v(message):
    thread = "w" # название треда
    cmd_func(message, thread)

@bot.message_handler(commands=['wg'])
def update_vg(message):
    thread = "wg" # название треда
    cmd_func(message, thread)

@bot.message_handler(commands=['wsr'])
def update_wsr(message):
    thread = "wsr" # название треда
    cmd_func(message, thread)
    
def telegram_polling():
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e: 
        print("СБОЙ ПОДКЛЮЧЕНИЯ!")
        print(e)
        print("Пробую реконнект...")
        bot.stop_polling()
        time.sleep(3)
        telegram_polling()
telegram_polling()
        
"""
        
# Это нужно для того, чтобы все время опрашивать бота на наличие сообщений от пользователя        
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e: 
        print("СБОЙ ПОДКЛЮЧЕНИЯ!")
        print(e)
        
"""        