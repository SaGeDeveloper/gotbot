'''

команды перед игрой:
/начнем - /start
/зарандомитьдома - /random_houses
/зарандомитьпорядок - /random_poriadok
/закрепитьроли - /consolidate_roles
команды для игры:
/открытьприказы - /open_orders
/открытьставки - /open_bids
/открытьвестерос - /open_vesteros
/открытьдичь - /open_wildlings
/торги - /bidding
/ворона - /crow
/убратькарты - /delete_cards
/открытькарты - /open_cards

* по командам "/*название дома*" понять какой игрок за кого играет (названия домов: старк, грей, лани, бара, март, тир) +
    * по команде "/закрепитьдома" отключить возможность выбирать дома ++
    * по команде "/начнем" сделать чат в котором была это команда основным ++

* запрашивать сообщение с приказами по команде "/отдатьприказы" +
    * удалять приказы игрока по команде "/убратьприказы" +
    * присылать приказы по команде "/открытьприказы" +

* присылать 3 карты вестроса по команде "/открытьвестерос" +

* присылать карты одичалых по команде "/открытьдичь" +

* по команде "/поставитькарту" бот запрашивает сообщение с картой +
    * по команде "/открытькарты" бот открывает карты +
    * по команде "/сменитькарты" бот забывает поставленные карты +

* запросить команду "/сделатьставку" у всех игроков по команде "/торги" +
    * по команде "/сделатьставку" бот запрашивает ставку +
    * по команде "/открытьставки" бот открывает ставки +
    * по команде "/убратьставку" бот убирает ставку +

* по команде "/ворона" проверять наличие ворона у данного игрока
    * по команде "/ошибка" отменять проверку
    * по командам /закопать или /оставить закапывать или оставлять карту одичалых

в списках, которые имитируют колоды карт я считаю, что нулевой элемент списка является верхней картой колоды
'''

houses = dict()


def allcases(arr):
    arr2 = []
    for i in arr:
        arr2.append(i)
        arr2.append(i.upper())
        arr2.append(i[0].upper()+i[1:])
        arr2.append(i[0] + i[1:].upper())
    return arr2


lannister_names = allcases(["лани", "ланни", "ланнистер", "ланистер", 'lannister', 'lani'])
stark_names = allcases(['старк', "болтон", 'stark', 'bolton'])
bara_names = allcases(['бара', "баратеон", 'bara', 'barateon'])
grey_names = allcases(['грей', "грейджой", 'grey', 'greyjoy'])
tir_names = allcases(['тир', "тирелл", 'tir', 'tirell', 'tyr', 'tyrell'])
mart_names = allcases(['март', "мартелл", 'mart', 'martell'])

lani_cards = "Тайвин Ланнистер (4).Сер Грегор Клиган (3).Пёс (2).Сер Джейме Ланнистер (2).Тирион Ланнистер (1).Сер Киван Ланнистер (1).Серсея Ланнистер (0)".split(".")
stark_cards = "Эддард Старк (4).Робб Старк (3).Джон Амбер (2).Русе Болтон (2).Бринден черная рыба (1).Сер Родрик Кассель (1).Кейтилин Старк (0)".split(".")
bara_cards = "Станнис Баратеон (4).Ренли Баратеон (3).Сер Давос Сиворт (2).Бриенна Тарт (2).Саладор Саан (1).Мелисандра (1).Пестряк (0)".split(".")
grey_cards = "Эурон Грейджой (4).Виктарион Грейджой (3).Бейлон Грейджой (2).Теон Грейджой (2).Дагмер Щербатый (1).Аша Грейджой (1).Эйерон Грейджой (0)".split(".")
tir_cards = "Мейс Тирелл (4).Лорас Тирелл (3).Рендилл Тарли (2).Гарлан Тирелл (2).Маргери Тирелл (1).Алесер Флорент (1).Королева Шипов (0)".split(".")
mart_cards = "Оберин Красный Змей (4).Арео Хотах (3).Герольд Темная Звезда (2).Обара Сэнд (2).Арианна Мартелл (1).Нимерия Сэнд (1).Доран Мартелл (0)".split(".")

import telebot
import random
from telebot import types
bot = telebot.TeleBot('1881455002:AAGZgq6ZbQRR_OMubEXWpfzq5aD-d8DtT_Y')

# реализация команды "/зарандомитьпорядок"
@bot.message_handler(commands=['зарандомитьпорядок', 'random_poriadok'])
def random_poriadok_krytoi(m):
    global sp1
    if m.from_user.id in players_list_for_random_houses:
        if m.chat.id == chat1:
            if not roles_assigned:
                if len(players_list_for_random_houses) == 6:
                    sp1.sort(key=lambda a: random.random())
                    bot.send_message(chat1, 'Порядок выбора домов:\n1. @{}\n2. @{}\n3. @{}\n4. @{}\n5. @{}\n6. @{}'.format(sp1[0][0], sp1[1][0], sp1[2][0], sp1[3][0], sp1[4][0], sp1[5][0]))
                else:
                    bot.send_message(chat1, 'Недостаточно игроков: ' + str(len(players_list_for_random_houses)) + '/6')
            else:
                bot.send_message(chat1, 'Дома уже распределены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

# реализация команды "/зарандомитьдома"
players_list_for_random_houses = set()
@bot.message_handler(commands=['зарандомитьдома', 'random_houses'])
def random_houses_function(m):
    global sp1, players_list_for_random_houses, lani, lani_name, stark, stark_name, bara, bara_name, grey, grey_name, tir, tir_name, mart, mart_name
    if m.from_user.id in players_list_for_random_houses:
        if m.chat.id == chat1:
            if not roles_assigned:
                if len(players_list_for_random_houses) == 6:
                    sp1.sort(key=lambda a: random.random())
                    lani = sp1[0][0]; lani_name = sp1[0][1]; houses[lani] = 'Ланнистер'
                    bot.send_message(lani, 'Привет, Ланнистер!')
                    stark = sp1[1][0]; stark_name = sp1[1][1]; houses[stark] = 'Старк'
                    bot.send_message(stark, 'Привет, Старк!')
                    bara = sp1[2][0]; bara_name = sp1[2][1]; houses[bara] = 'Баратеон'
                    bot.send_message(bara, 'Привет, Баратеон!')
                    grey = sp1[3][0]; grey_name = sp1[3][1]; houses[grey] = 'Грейджой'
                    bot.send_message(grey, 'Привет, Грейджой!')
                    tir = sp1[4][0]; tir_name = sp1[4][1]; houses[tir] = 'Тирелл'
                    bot.send_message(tir, 'Привет, Тирелл!')
                    mart = sp1[5][0]; mart_name = sp1[5][1]; houses[mart] = 'Мартелл'
                    bot.send_message(mart, 'Привет, Мартелл!')
                    bot.send_message(chat1,
                                     'Дома зарандомлены:\nЛаннистер - @{}\nСтарк - @{}\nБаратеон - @{}\nГрейджой - @{}\nТирелл - @{}\nМартелл - @{}\n\nТеперь можете использовать команду /закрепитьдома - /consolidate_roles'.format(
                                         lani_name, stark_name, bara_name, grey_name, tir_name, mart_name))
                else:
                    bot.send_message(m.chat.id, 'Недостаточно игроков: ' + str(len(players_list_for_random_houses)) + '/6')
            else:
                bot.send_message(chat1, 'Дома уже закреплены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

# реализация отслеживания новых пользователей чата


# реализация команды "/игрок"
sp1 = []
@bot.message_handler(commands=['игрок', 'player'])
def player(m):
    if m.chat.id == chat1:
        if not roles_assigned:
            if not m.from_user.id in players_list_for_random_houses:
                if len(players_list_for_random_houses) != 6:
                    players_list_for_random_houses.add(m.from_user.id)
                    sp1.append([m.from_user.id, m.from_user.username])
                    bot.send_message(m.chat.id, 'Теперь @' + m.from_user.username + ' игрок. Обязательно напиши мне в лс любое сообщение(не команду)')
                else:
                    bot.send_message(m.chat.id, 'Сейчас уже есть 6 игроков. Можете попросить игрока стать зрителем. Для этого он должен написать команду /зритель - /viewer')
            else:
                bot.send_message(m.chat.id, 'Вы уже являетесь игроком')
        else:
            bot.send_message(m.chat.id, 'Роли уже закреплены')
    else:
        bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')

# реализация команды "/зритель"
@bot.message_handler(commands=['зритель', 'viewer'])
def player(m):
    if m.chat.id == chat1:
        if m.from_user.id in players_list_for_random_houses:
            players_list_for_random_houses.remove(m.from_user.id)
            sp1.remove([m.from_user.id, m.from_user.username])
        bot.send_message(m.chat.id, 'Теперь @' + m.from_user.username + ' зритель')
    else:
        bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')

# реализация команды "/закрепитьдома"
roles_assigned = False
can_send_yes = False
@bot.message_handler(commands = ['закрепитьдома', 'consolidate_roles'])
def f200(m):
    if m.from_user.id in players_list_for_random_houses:
        global roles_assigned, can_send_yes
        if m.chat.id == chat1:
            if not roles_assigned:
                kb_proverka = types.InlineKeyboardMarkup()
                k_proverka = types.InlineKeyboardButton(text='Все верно', callback_data='все верно')
                kb_proverka.add(k_proverka)
                bot.send_message(chat1, 'Убедитесь, что дома выбраны верно:\nЛаннистер - @{}\nСтарк - @{}\nБаратеон - @{}\nГрейджой - @{}\nТирелл - @{}\nМартелл - @{}'.format(lani_name, stark_name, bara_name, grey_name, tir_name, mart_name), reply_markup=kb_proverka)
                can_send_yes = True
            else:
                bot.send_message(chat1, 'Дома уже закреплены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

@bot.message_handler(content_types=['new_chat_members'])
def new_chat_members(m):
    if m.chat.id == chat1:
        if not roles_assigned:
            bot.send_message(chat1, 'Привет, напишите кем вы являетесь, /игрок - /player или /зритель - /viewer')
        else:
            bot.send_message(chat1, 'Игра уже началась. Вы являетесь зрителем')
    else:
        bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')

# реализация знакомства бота с игроками
stark_name = lani_name = mart_name = tir_name = bara_name = grey_name = ''
stark = lani = mart = tir = bara = grey = chat1 = 0 # id игроков
bool_chat1 = False
@bot.message_handler(commands=['начнем', 'start'])
def f107(m):
    global chat1, bool_chat1
    if not bool_chat1:
        chat1 = m.chat.id
        bool_chat1 = True
        bot.send_message(chat1, 'Начнем игру! Данный чат является глобальным')
    else:
        bot.send_message(m.chat.id, 'глобальный чат уже выбран. Чтобы его изменить нужно перезапустить бота')
@bot.message_handler(commands=stark_names)
def f0(m):
    if m.from_user.id in players_list_for_random_houses:
        global stark, stark_name
        if m.chat.id == chat1:
            if not roles_assigned:
                stark = m.from_user.id
                houses[m.from_user.id] = "Cтарк"
                stark_name = m.from_user.username
                bot.send_message(stark, 'Привет, Старк!')
                bot.send_message(m.chat.id, 'теперь @' + m.from_user.username + ' старк')
            else:
                bot.send_message(m.chat.id, 'Дома уже распределены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
@bot.message_handler(commands=lannister_names)
def f1(m):
    if m.from_user.id in players_list_for_random_houses:
        global lani, lani_name
        if m.chat.id == chat1:
            if not roles_assigned:
                lani = m.from_user.id
                houses[m.from_user.id] = "Ланнистер"
                lani_name = m.from_user.username
                bot.send_message(lani, 'Привет, Ланнистер!')
                bot.send_message(m.chat.id, 'теперь @' + m.from_user.username + ' ланнистер')
            else:
                bot.send_message(m.chat.id, 'Дома уже распределены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
@bot.message_handler(commands=mart_names)
def f2(m):
    if m.from_user.id in players_list_for_random_houses:
        global mart, mart_name
        if m.chat.id == chat1:
            if not roles_assigned:
                mart = m.from_user.id
                houses[m.from_user.id] = "Мартелл"
                mart_name = m.from_user.username
                bot.send_message(mart, 'Привет, Мартелл!')
                bot.send_message(m.chat.id, 'теперь @' + m.from_user.username + ' мартелл')
            else:
                bot.send_message(m.chat.id, 'Дома уже распределены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
@bot.message_handler(commands=tir_names)
def f3(m):
    if m.from_user.id in players_list_for_random_houses:
        global tir, tir_name
        if m.chat.id == chat1:
            if not roles_assigned:
                tir = m.from_user.id
                houses[m.from_user.id] = "Тирелл"
                tir_name = m.from_user.username
                bot.send_message(tir, 'Привет, Тирелл!')
                bot.send_message(m.chat.id, 'теперь @' + m.from_user.username + ' тирелл')
            else:
                bot.send_message(m.chat.id, 'Дома уже распределены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
@bot.message_handler(commands=bara_names)
def f4(m):
    if m.from_user.id in players_list_for_random_houses:
        global bara, bara_name
        if m.chat.id == chat1:
            if not roles_assigned:
                bara = m.from_user.id
                houses[m.from_user.id] = "Баратеон"
                bara_name = m.from_user.username
                bot.send_message(bara, 'Привет, Баратеон!')
                bot.send_message(m.chat.id, 'теперь @' + m.from_user.username + ' баратеон')
            else:
                bot.send_message(m.chat.id, 'Дома уже распределены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
@bot.message_handler(commands=grey_names)
def f5(m):
    if m.from_user.id in players_list_for_random_houses:
        global grey, grey_name
        if m.chat.id == chat1:
            if not roles_assigned:
                grey = m.from_user.id
                houses[m.from_user.id] = "Грейджой"
                grey_name = m.from_user.username
                bot.send_message(grey, 'Привет, Грейджой!')
                bot.send_message(m.chat.id, 'теперь @' + m.from_user.username + ' грейджой')
            else:
                bot.send_message(m.chat.id, 'Дома уже распределены')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

# реализация команды "/открытьвестерос"
deck1 = ['Последние дни лета', 'Сбор войск', 'Сбор войск', 'Сбор войск', 'Снабжение', 'Снабжение', 'Снабжение', 'Трон из клинков', 'Трон из клинков', 'Зима близко'] # 1-ая колода вестероса
deck2 = ['Последние дни лета', 'Битва королей', 'Битва королей', 'Битва королей', 'Игра престолов', 'Игра престолов', 'Игра престолов', 'Черные крылья, черные слова', 'Черные крылья, черные слова', 'Зима близко'] # 2-ая колода вестероса
deck3 = ['Преданы мечу', 'Преданы мечу', 'Нашествие одичалых', 'Нашествие одичалых', 'Нашествие одичалых', 'Буря мечей', 'Дожди осени', 'Море штормов', 'Паутина лжи', 'Пир для ворон'] # 3-ая колода вестероса
deck1.sort(key=lambda a: random.random()) # перемешиваем 1-ую колоду вестероса
deck2.sort(key=lambda a: random.random()) # перемешиваем 2-ую колоду вестероса
deck3.sort(key=lambda a: random.random()) # перемешиваем 3-ю колоду вестероса
confirm_open_vesteros = set()
@bot.message_handler(commands=['открытьвестерос', 'open_vesteros'])
def f100(m):
    if m.from_user.id in players_list_for_random_houses:
        global confirm_open_vesteros
        if m.chat.id == chat1:
            confirm_open_vesteros.add(m.from_user.id)
            if len(confirm_open_vesteros) >= 3:
                confirm_open_vesteros = set()
                # проверка на карту "Зима близко" в 1-ой колоде вестероса
                winter_is_coming1 = ''
                while deck1[0] == 'Зима близко':
                    deck1.sort(key=lambda a: random.random())
                    winter_is_coming1 += 'Зима близко -> '
                # проверка на карту "Зима близко" во 2-ой колоде вестероса
                winter_is_coming2 = ''
                while deck2[0] == 'Зима близко':
                    deck2.sort(key=lambda a: random.random())
                    winter_is_coming2 += 'Зима близко -> '
                bot.send_message(m.chat.id, '1 колода вестероса: ' + winter_is_coming1 + deck1[0] + '\n2 колода вестероса: ' + winter_is_coming2 + deck2[0] +'\n3 колода вестероса: ' + deck3[0])
                deck1.insert(len(deck1), deck1[0]); deck1.pop(0) # перекладываем верхнюю карту 1-ой колоды вестероса под низ колоды
                deck2.insert(len(deck2), deck2[0]); deck2.pop(0) # перекладываем верхнюю карту 2-ой колоды вестероса под низ колоды
                deck3.insert(len(deck3), deck3[0]); deck3.pop(0) # перекладываем верхнюю карту 3-ой колоды вестероса под низ колоды
            else:
                bot.send_message(chat1, 'Чтобы открыть вестерос, нужно подтверждение от 3 или более игроков(подтверждением является команда /открытьвестерос или /open_vesteros)')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')


# реализация команды "/открытьдичь"
wild_deck = ['Тишина у Стены', 'Разбойники Гремучей Рубашки', 'Сбор на Молоководной', 'Разведчик-оборотень', 'Передовой отряд', 'Убийцы ворон', 'Наездники на мамонтах', 'Наступление орды', 'Король-за-Стеной'] # колода одичалых
wild_deck.sort(key=lambda a: random.random()) # перемешиваем колоду одичалых
confirm_open_wild = set()
@bot.message_handler(commands=['открытьдичь', 'open_wildlings'])
def f101(m):
    if m.from_user.id in players_list_for_random_houses:
        global confirm_open_wild
        if m.chat.id == chat1:
            confirm_open_wild.add(m.from_user.id)
            if len(confirm_open_wild) >= 3:
                confirm_open_wild = set()
                bot.send_message(m.chat.id, 'Карта одичалых: ' + wild_deck[0])
                wild_deck.insert(len(wild_deck), wild_deck[0]); wild_deck.pop(0) # перекладываем верхнюю карту колоды одичалых под низ колоды
            else:
                bot.send_message(chat1, 'Чтобы открыть карту одичалых, нужно подтверждение от 3 или более игроков(подтверждением является команда /открытьдичь или /open_wildlings)')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

# реализация команды "/открытьприказы"
@bot.message_handler(commands=['открытьприказы', 'open_orders'])
def f50(m):
    if m.from_user.id in players_list_for_random_houses:
        global stark_orders, lani_orders, bara_orders, mart_orders, grey_orders, tir_orders, \
            bool_ord_mart, bool_ord_tir, bool_ord_grey, bool_ord_stark, bool_ord_bara, bool_ord_lani
        if m.chat.id == chat1:
            c_ord = 0  # количество отданных приказов
            for i in [bool_ord_stark, bool_ord_lani, bool_ord_bara, bool_ord_tir, bool_ord_grey, bool_ord_mart]:
                c_ord += int(i)
            if c_ord == 6:
                for i in [stark_orders, lani_orders, bara_orders, tir_orders, grey_orders, mart_orders]:
                    bot.send_message(chat1, i)
                stark_orders = 'Приказы старка: \n'
                lani_orders = 'Приказы ланнистера: \n'
                mart_orders = 'Приказы мартелла: \n'
                tir_orders = 'Приказы тирелла: \n'
                bara_orders = 'Приказы баратеона: \n'
                grey_orders = 'Приказы грейджоя: \n'
                bool_ord_stark = False  # отдал ли старк приказы?
                bool_ord_lani = False  # отдал ли лани приказы?
                bool_ord_bara = False  # отдал ли бара приказы?
                bool_ord_mart = False  # отдал ли март приказы?
                bool_ord_grey = False  # отдал ли грей приказы?
                bool_ord_tir = False  # отдал ли тир приказы?
            else:
                bot.send_message(chat1, 'Пока еще не все отдали приказы. ' + str(c_ord) + '/6')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

# реализация команды "/отдатьприказы"
stark_orders = 'Приказы старка: \n'
lani_orders = 'Приказы ланнистера: \n'
mart_orders = 'Приказы мартелла: \n'
tir_orders = 'Приказы тирелла: \n'
bara_orders = 'Приказы баратеона: \n'
grey_orders = 'Приказы грейджоя: \n'
bool_ord_stark = False #отдал ли старк приказы?
bool_ord_lani = False #отдал ли лани приказы?
bool_ord_bara = False #отдал ли бара приказы?
bool_ord_mart = False #отдал ли март приказы?
bool_ord_grey = False #отдал ли грей приказы?
bool_ord_tir = False #отдал ли тир приказы?
@bot.message_handler(commands=['отдатьприказы', 'send_orders'])
def f75(m):
    if m.from_user.id in players_list_for_random_houses:
        if m.chat.id != chat1:
            if m.from_user.id == stark and not bool_ord_stark:
                bot.send_message(stark, 'напиши их мне одним сообщением')
                bot.register_next_step_handler(m, f150)
            elif m.from_user.id == lani and not bool_ord_lani:
                bot.send_message(lani, 'напиши их мне одним сообщением')
                bot.register_next_step_handler(m, f150)
            elif m.from_user.id == bara and not bool_ord_bara:
                bot.send_message(bara, 'напиши их мне одним сообщением')
                bot.register_next_step_handler(m, f150)
            elif m.from_user.id == grey and not bool_ord_grey:
                bot.send_message(grey, 'напиши их мне одним сообщением')
                bot.register_next_step_handler(m, f150)
            elif m.from_user.id == tir and not bool_ord_tir:
                bot.send_message(tir, 'напиши их мне одним сообщением')
                bot.register_next_step_handler(m, f150)
            elif m.from_user.id == mart and not bool_ord_mart:
                bot.send_message(mart, 'напиши их мне одним сообщением')
                bot.register_next_step_handler(m, f150)
            else:
                bot.send_message(m.from_user.id, 'вы уже отдали приказы. Если хотите их изменить напишите команду /убратьприказы - /delete_orders')
        else:
            bot.send_message(m.chat.id, 'данную команду лучше не использовать в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

def f150(m):
    global stark_orders, lani_orders, bara_orders, mart_orders, grey_orders, tir_orders, \
        bool_ord_mart, bool_ord_tir, bool_ord_grey, bool_ord_stark, bool_ord_bara, bool_ord_lani
    s = m.text
    if m.from_user.id == stark:
        stark_orders += s
        bool_ord_stark = True
        bot.send_message(stark, 'Ваши приказы приняты')
    if m.from_user.id == lani:
        lani_orders += s
        bool_ord_lani = True
        bot.send_message(lani, 'Ваши приказы приняты')
    if m.from_user.id == bara:
        bara_orders += s
        bool_ord_bara = True
        bot.send_message(bara, 'Ваши приказы приняты')
    if m.from_user.id == tir:
        tir_orders += s
        bool_ord_tir = True
        bot.send_message(tir, 'Ваши приказы приняты')
    if m.from_user.id == grey:
        grey_orders += s
        bool_ord_grey = True
        bot.send_message(grey, 'Ваши приказы приняты')
    if m.from_user.id == mart:
        mart_orders += s
        bool_ord_mart = True
        bot.send_message(mart, 'Ваши приказы приняты')
    c_ord1 = 0  # количество отданных приказов
    for i in [bool_ord_stark, bool_ord_lani, bool_ord_bara, bool_ord_tir, bool_ord_grey, bool_ord_mart]:
        c_ord1 += int(i)
    bot.send_message(chat1, 'Приказы ' + str(c_ord1) + '/6')
# Код продвинутых колод (тест)
# ======================================
class Player:
    id = 0
    role = ""
class Card:
    def __init__(self, _owner, _names, _power, _swords, _towers, _priority):
        self.owner = 0
        self.names = []
        self.power = 0
        self.swords = 0
        self.towers = 0
        self.priority = 0
    def text(self):
        pass

# приоритеты
# 0 - игнорируйте, отмените
# 1 - немедленно
# 2 - обычные свойства
# 3 - после боя
# все карты классики
# баратеон
bara_k_0 = Card(bara, 'Пестряк (0)', 0, 0, 0, 3)
bara_k_1_1 = Card(bara, 'Мелисандра (1)', 1, 1, 0, 2)
bara_k_1_2 = Card(bara, 'Салладор Саан (1)', 1, 0, 0, 2)
bara_k_2_1 = Card(bara, 'Бриенна Тарт (2)', 2, 1, 1, 2)
bara_k_2_2 = Card(bara, 'Сер Давос Сиворт (2)', 2, 0, 0, 2)
bara_k_3 = Card(bara, 'Ренли Баратеон (3)', 3, 0, 0, 3)
bara_k_4 = Card(bara, 'Станнис Баратеон (4)', 4, 0, 0, 2)
# Ланнистер
lani_k_0 = Card(lani, 'Серсея Ланнистер (0)', 0, 0, 0, 3)
lani_k_1_1 = Card(lani, 'Тирион Ланнистер (1)', 1, 0, 0, 1)
lani_k_1_2 = Card(lani, 'Сер Киван Ланнистер (1)', 1, 0, 0, 2)
lani_k_2_1 = Card(lani, 'Сер Джейме Ланнистер (2)', 2, 1, 0, 2)
lani_k_2_2 = Card(lani, 'Пес (2)', 2, 0, 2, 2)
lani_k_3 = Card(lani, 'Сер Грегор Клиган (3)', 3, 3, 0, 2)
lani_k_4 = Card(lani, 'Тайвин Ланнистер (4)', 4, 0, 0, 3)
# Старк
stark_k_0 = Card(stark, 'Кейтилин Старк (0)', 0, 0, 0, 2)
stark_k_1_1 = Card(stark, 'Сер Родрик Кассель (1)', 1, 0, 2, 2)
stark_k_1_2 = Card(stark, 'Бринден Черная Рыба (1)', 1, 0, 0, 2)
stark_k_2_1 = Card(stark, 'Большой Джон Амбер (2)', 2, 1, 0, 2)
stark_k_2_2 = Card(stark, 'Русе Болтон (2)', 2, 0, 0, 3)
stark_k_3 = Card(stark, 'Робб Старк (3)', 3, 0, 0, 3)
stark_k_4 = Card(stark, 'Эддард Старк (4)', 4, 2, 0, 2)
# Мартелл
mart_k_0 = Card(mart, 'Доран Мартелл (0)', 0, 0, 0, 1)
mart_k_1_1 = Card(mart, 'Нимерия Сэнд (1)', 1, 0, 0, 2)
mart_k_1_2 = Card(mart, 'Арианна Мартелл (1)', 1, 0, 0, 3)
mart_k_2_1 = Card(mart, 'Герольд Темная Звезда (2)', 2, 1, 0, 2)
mart_k_2_2 = Card(mart, 'Обара Сэнд (2)', 2, 1, 0, 2)
mart_k_3 = Card(mart, 'Арео Хота (3)', 3, 0, 1, 2)
mart_k_4 = Card(mart, 'Оберин Красная Гадюка (4)', 4, 2, 1, 2)
# грейджой
grey_k_0 = Card(grey, 'Эйерон Сыровласый (0)', 0, 0, 0, 1)
grey_k_1_1 = Card(grey, 'Аша Грейджой (1)', 1, 0, 0, 2)
grey_k_1_2 = Card(grey, 'Дагмер Битый Рот (1)', 1, 1, 1, 2)
grey_k_2_1 = Card(grey, 'Теон Грейджой (2)', 2, 0, 0, 2)
grey_k_2_2 = Card(grey, 'Бейлон Грейджой (6)', 2, 0, 0, 2)
grey_k_3 = Card(grey, 'Виктарион Грейджой (3)', 3, 0, 0, 2)
grey_k_4 = Card(grey, 'Эурон Вороний Глаз (4)', 4, 1, 0, 2)
# Старк
tir_k_0 = Card(tir, 'Королева Шипов (0)', 0, 0, 0, 1)
tir_k_1_1 = Card(tir, 'Алестер Флорент (1)', 1, 0, 1, 2)
tir_k_1_2 = Card(tir, 'Маргери Тирелл (1)', 1, 0, 1, 2)
tir_k_2_1 = Card(tir, 'Сер Гарлан Тирелл (2)', 2, 2, 0, 2)
tir_k_2_2 = Card(tir, 'Рэндил Тарли(2)', 2, 1, 0, 2)
tir_k_3 = Card(tir, 'Сер Лорса Тирелл (3)', 3, 0, 0, 3)
tir_k_4 = Card(tir, 'Мейс Тирелл (4)', 4, 0, 0, 1)


atk = 0
dfs = 0
atk_text_resolved = 0
dfs_text_resolved = 0
resolving_atk = 0
atk_card = 0 # Изменится на Card
dfs_card = 0 # Изменится на Card
def combatResolve(atk_card, dfs_card):
    global resolving_atk
    if atk_card.priority >= dfs_card.priority:
        resolving_atk = 1
    while not (atk_text_resolved and dfs_text_resolved):
        if resolving_atk:
            atk_card.text()
        else:
            dfs_card.text()
    resolving_atk = 1 - resolving_atk
# ======================================

# НОВАЯ реализация команды "/поставитькарту"
battle_sides = 0
battle_cards = dict()
@bot.message_handler(commands=['поставитькарту', 'send_card'])
def event_setcard(m):
    if m.from_user.id in players_list_for_random_houses:
        global battle_sides
        if m.chat.id != chat1:
            if battle_sides < 2:
                battle_sides += 1
                kb = types.InlineKeyboardMarkup()
                if m.from_user.id == stark:
                    cardlist = stark_cards
                if m.from_user.id == lani:
                    cardlist = lani_cards
                if m.from_user.id == bara:
                    cardlist = bara_cards
                if m.from_user.id == grey:
                    cardlist = grey_cards
                if m.from_user.id == tir:
                    cardlist = tir_cards
                if m.from_user.id == mart:
                    cardlist = mart_cards
                k0 = types.InlineKeyboardButton(text=cardlist[0], callback_data=cardlist[0])
                kb.add(k0)
                k1 = types.InlineKeyboardButton(text=cardlist[1], callback_data=cardlist[1])
                kb.add(k1)
                k2 = types.InlineKeyboardButton(text=cardlist[2], callback_data=cardlist[2])
                kb.add(k2)
                k3 = types.InlineKeyboardButton(text=cardlist[3], callback_data=cardlist[3])
                kb.add(k3)
                k4 = types.InlineKeyboardButton(text=cardlist[4], callback_data=cardlist[4])
                kb.add(k4)
                k5 = types.InlineKeyboardButton(text=cardlist[5], callback_data=cardlist[5])
                kb.add(k5)
                k6 = types.InlineKeyboardButton(text=cardlist[6], callback_data=cardlist[6])
                kb.add(k6)

                bot.send_message(m.chat.id, text='Выберите карту', reply_markup=kb)
            else:
                bot.send_message(m.from_user.id, 'Нельзя поставить карту, так как еще идет какой-то бой')
        else:
            bot.send_message(m.chat.id, 'Эту команду лучше не использовать в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
@bot.callback_query_handler(func=lambda call: True)
def setcard(call):
    global battle_cards, roles_assigned
    if call.data in bara_cards or call.data in stark_cards or call.data in lani_cards or call.data in grey_cards or call.data in tir_cards or call.data in mart_cards:
        battle_cards[call.from_user.id] = call.data
        bot.send_message(call.from_user.id, 'Вы поставили ' + call.data)
    if call.data == 'все верно':
        if not roles_assigned:
            roles_assigned = True
            bot.send_message(chat1, 'Дома успешно закреплены за участниками')
            for i in [lani, stark, mart, tir, bara, grey]:
                bot.send_message(i, 'Команды для игрока\n/отдатьприказы - /send_orders\n/поставитькарту - /send_card\n/сделатьставку - /send_bid \n/убратьприказы - /delete_orders\n/убратьставку - /delete_bid\n/оставить - /avna_loh\n/закопать - /bury')
                bot.send_message(i, 'Советую закрепить это сообщение')
        else:
            bot.send_message(chat1, 'Дома уже закреплены')



# реализация команды "/открытькарты"
@bot.message_handler(commands=['открытькарты', 'open_cards'])
def f500(m):
    if m.from_user.id in players_list_for_random_houses:
        global battle_cards
        if m.chat.id == chat1:
            if len(battle_cards) == 2:
                for i in list(battle_cards.keys()):
                    bot.send_message(chat1, houses[i] + " поставил карту " + battle_cards[i])
                battle_cards = dict()
            else:
                bot.send_message(chat1, 'карты поставили ' + str(len(battle_cards)) + '/2')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

# реализация команды "/сменитькарты"
@bot.message_handler(commands=['сменитькарты', 'delete_cards'])
def f100(m):
    if m.from_user.id in players_list_for_random_houses:
        global  battle_cards
        if m.chat.id == chat1:
            battle_cards = []
            bot.send_message(chat1, 'Карты боя обоих игроков отменены. Теперь можно снова использовать команду /поставитькарту - /send_card')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

# реализация команды "/убратьприказы"
@bot.message_handler(commands=['убратьприказы', 'delete_orders'])
def f600(m):
    if m.from_user.id in players_list_for_random_houses:
        global stark_orders, lani_orders, bara_orders, mart_orders, grey_orders, tir_orders, \
            bool_ord_mart, bool_ord_tir, bool_ord_grey, bool_ord_stark, bool_ord_bara, bool_ord_lani
        if m.from_user.id == stark:
            stark_orders = 'Приказы старка: \n'; bool_ord_stark = False
        if m.from_user.id == lani:
            lani_orders = 'Приказы ланнистера: \n'; bool_ord_lani = False
        if m.from_user.id == bara:
            bara_orders = 'Приказы баратеона: \n'; bool_ord_bara = False
        if m.from_user.id == mart:
            mart_orders = 'Приказы мартелла: \n'; bool_ord_mart = False
        if m.from_user.id == grey:
            grey_orders = 'Приказы грейджоя: \n'; bool_ord_grey = False
        if m.from_user.id == tir:
            tir_orders = 'Приказы тирелла: \n'; bool_ord_tir = False
        bot.send_message(m.from_user.id, 'Ваши приказы убраны. Вы можете вновь воспользоваться командой /отдатьприказы - /send_orders')
        c_ord2 = 0  # количество отданных приказов
        for i in [bool_ord_stark, bool_ord_lani, bool_ord_bara, bool_ord_tir, bool_ord_grey, bool_ord_mart]:
            c_ord2 += int(i)
        bot.send_message(chat1, 'Приказы ' + str(c_ord2) + '/6')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')




# реализация команды "/торги"
current_track = 0
TRACK_NAMES = [0,"Железный Трон","Валирийский Меч","Посыльного ворона"]
@bot.message_handler(commands=['торги', 'bidding'])
def f1000(m):
    global current_track
    if m.from_user.id in players_list_for_random_houses:
        if m.chat.id == chat1:
            if current_track == 0:
                current_track += 1
                bidding_round()
            else:
                bot.send_message(chat1, 'Торги уже идут')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

def bidding_round():
    global current_track
    if current_track >= 4:
        bot.send_message(chat1, 'Торги окончены!')
        current_track = 0
        return
    bot.send_message(chat1, f'Начинаем торги за {TRACK_NAMES[current_track]}!')
    for i in [stark, bara, grey, lani, mart, tir]:
        if i != 0:
            bot.send_message(i, f'Начались торги за {TRACK_NAMES[current_track]}. Вооспользуйтесь командой /сделатьставку - /send_bid, чтобы сделать ставку')

# реализация команды "/сделатьставку"
bid_lani = bid_stark = bid_grey = bid_bara = bid_tir = bid_mart = ['NULL']
#bool_bid_lani = bool_bid_stark = bool_bid_grey = bool_bid_bara = bool_bid_tir = bool_bid_mart = False
bids = set()
@bot.message_handler(commands=['сделатьставку', 'send_bid'])
def f1500(m):
    if m.from_user.id in players_list_for_random_houses:
        if m.chat.id != chat1:
            if current_track:
                if m.from_user.id in bids:
                    bot.send_message(m.from_user.id, 'Вы уже сделали ставку. Используйте команду /убратьставку - /delete_bid, чтобы изменить ее')
                else:
                    bot.send_message(m.chat.id, 'Напиши мне ставку одним сообщением')
                    bot.register_next_step_handler(m, f6)
            else:
                bot.send_message(m.from_user.id, 'Сейчас нет активных торгов')
        else:
            bot.send_message(m.chat.id, 'Эту команду лучше не использовать в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
def f6(m):
    global bid_lani, bid_stark, bid_grey, bid_bara, bid_tir, bid_mart
    bid = m.text
    if bid.isdigit():
        bids.add(m.from_user.id)
        if m.from_user.id == lani:
            bid_lani = ['Ставка ланнистера: ', bid]
        if m.from_user.id == stark:
            bid_stark = ['Ставка старка: ' , bid]
        if m.from_user.id == grey:
            bid_grey = ['Ставка грейджоя: ' , bid]
        if m.from_user.id == bara:
            bid_bara = ['Ставка баратеона: ' , bid]
        if m.from_user.id == tir:
            bid_tir = ['Ставка тирелла: ' , bid]
        if m.from_user.id == mart:
            bid_mart = ['Ставка мартелла: ' , bid]
        bot.send_message(m.from_user.id, 'Ваша ставка принята')
        bot.send_message(chat1, 'Ставки ' + str(len(bids)) + '/6')
    else:
        bot.send_message(m.from_user.id, 'Ставка должна быть целым числом не меньше нуля')

# реализация команды "/открытьставки"
@bot.message_handler(commands=['открытьставки', 'open_bids'])
def f01(m):
    if m.from_user.id in players_list_for_random_houses:
        global current_track, bids
        if m.chat.id == chat1:
            if current_track:
                if len(bids) == 2:
                    for i in [bid_lani, bid_stark, bid_grey, bid_bara, bid_tir, bid_mart]:
                        bot.send_message(chat1, "".join(i))
                    current_track += 1
                    bidding_round()
                    bids = set()
                else:
                    bot.send_message(chat1, 'Еще не все сделали ставки. ' + str(len(bids)) + '/6')
            else:
                bot.send_message(chat1, 'Сейчас нет активных торгов')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
# реализация команды "/убратьставку"
@bot.message_handler(commands=['убратьставку', 'delete_bid'])
def f02(m):
    if current_track:
        if m.from_user.id in players_list_for_random_houses:
            if m.from_user.id in bids:
                bids.remove(m.from_user.id)
            bot.send_message(m.from_user.id, 'Ваша ставка успешно удалена. Теперь вы снова можете использовать команду /сделатьставку - /send_bid')
            bot.send_message(chat1, 'Ставки ' + str(len(bids)) + '/6')
        else:
            bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')
    else:
        bot.send_message(chat1, 'Сейчас нет активных торгов')

# реализация команды "/ворона"
true_crow = 0
crow = 0
test_crow = False
test_crow_set = set()
@bot.message_handler(commands=['ворона', 'crow'])
def f03(m):
    if m.from_user.id in players_list_for_random_houses:
        global crow, test_crow, test_crow_set
        if m.chat.id == chat1:
            if not test_crow:
                crow = m.from_user.id
                test_crow_set.add(m.from_user.id)
                bot.send_message(chat1, 'Если 2 других игрока напишут команду /подтверждаю - /confirm, то вам будет выдана карта одичалых. Если у вас нет вороны, то напишите /ошибка - /mistake')
                test_crow = True
            else:
                bot.send_message(chat1, 'Кто-то уже хочет использовать ворону')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

@bot.message_handler(commands=['подтверждаю', 'confirm'])
def f04(m):
    if m.from_user.id in players_list_for_random_houses:
        global true_crow
        if m.chat.id == chat1:
            if test_crow:
                if not(m.from_user.id in test_crow_set):
                    test_crow_set.add(m.from_user.id)
                    bot.send_message(chat1, 'Подтверждений ' + str(len(test_crow_set) - 1) + '/2')
                    if len(test_crow_set) == 3:
                        true_crow = crow
                        bot.send_message(chat1, 'Ворон подтвержден. Отправляю его владельцу карту одичалых ')
                        bot.send_message(crow, 'Карта одичалых: ' + wild_deck[0])
                        bot.send_message(crow, 'Выберете, что сделать с этой картой: \n1. /закопать - /bury\n2. /оставить - /avna_loh')
                else:
                    bot.send_message(chat1, 'Вы уже подтвердили, что использование ворона законно')
            else:
                bot.send_message(chat1, 'Сейчас никто не хочет использовать ворону')
        else:
            bot.send_message(m.chat.id, 'Эту команду можно использовать только в глобальном чате')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

@bot.message_handler(commands=['закопать', 'bury'])
def f001(m):
    if m.from_user.id in players_list_for_random_houses:
        global test_crow_set, test_crow, true_crow
        if m.from_user.id == true_crow:
            wild_deck.insert(len(wild_deck), wild_deck[0])
            wild_deck.pop(0)
            bot.send_message(chat1, 'Владелец ворона решил положить карту одичалых под низ колоды')
            test_crow_set = set(); test_crow = False; true_crow = 0
        else:
            bot.send_message(m.chat.id, 'У вас не подтвержден жетон посыльного ворона, так что вы не можете использовать эту команду')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

@bot.message_handler(commands=['оставить', 'avna_loh'])
def f001(m):
    if m.from_user.id in players_list_for_random_houses:
        global test_crow_set, test_crow, true_crow
        if m.from_user.id == true_crow:
            bot.send_message(chat1, 'Владелец ворона решил оставить карту одичалых наверху колоды')
            test_crow_set = set(); test_crow = False; true_crow = 0
        else:
            bot.send_message(m.chat.id, 'У вас не подтвержден жетон посыльного ворона, так что вы не можете использовать эту команду')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

@bot.message_handler(commands=['ошибка', 'mistake'])
def f001(m):
    if m.from_user.id in players_list_for_random_houses:
        global test_crow_set, test_crow
        test_crow_set = set()
        test_crow = False
        bot.send_message(m.chat.id, 'Хорошо, играем дальше')
    else:
        bot.send_message(m.chat.id, 'Вы не игрок, поэтому не имеете права использовать команды')

bot.polling()