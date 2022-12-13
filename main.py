import asyncio
import logging
import aiohttp
import socket
import ssl
import datetime
import csv
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
import config

"""import configparser


config = configparser.ConfigParser()
config.read('configfile.ini')"""

API_TOKEN = config.API_TOKEN
# Configure logging
logging.basicConfig(level=logging.INFO)

"""
set_time_up - таймер для мон.сайтів, див. help
set_time_ssl - таймер для SSL сертф. див. help
up_nacp - почати моніторинг сайтів
ssl_check_nacp - почати моніторинг ssl
stop_ssl_check_nacp - зупинити моніторинг ssl
stop_up_nacp - зупинити моніторинг сайтів
help - пояснення для таймерів
"""

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

down_time = {  # СЮДИ ЗАПИСУЮТЬСЯ КЛЮЧІ(САЙТИ) З ДІКТА nacp_sites А ЗНАЧЕННЯ КЛЮЧІВ(САЙТІВ) - ЧАС КОЛИ
    # ВОНИ СТАЛИ НЕДОСТУПНІ, ЩОБ ПОТІМ МОЖНА БУЛО ВИРАХУВАТИ ДЕЛЬТУ ЧАСУ
}

nacp_sites = config.nacp_sites
nacp_sites_ssl = config.nacp_sites_ssl
time_for_up = config.time_for_up
time_for_ssl = config.time_for_ssl
WhileLoopFlag = config.WhileLoopFlag
WhileLoopFlag_nacp = config.WhileLoopFlag_nacp

with open('logout.csv', 'a+', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Назва операції', 'Результат', 'Час виконання: ДД/ММ/РР Год/Хв/Сек']
    logger = csv.DictWriter(csvfile, fieldnames=fieldnames)
    logger.writerow({'Назва операції': "Запуск скрипта", 'Результат': " LOADED",
                     'Час виконання: ДД/ММ/РР Год/Хв/Сек': (datetime.now()).strftime("%d:%m:%y %H:%M:%S")})


async def logger_writer(first_par, sec_par):
    with open('logout.csv', 'a+', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Назва операції', 'Результат', 'Час виконання: ДД/ММ/РР Год/Хв/Сек']
        logger = csv.DictWriter(csvfile, fieldnames=fieldnames)
        logger.writerow({'Назва операції': first_par, 'Результат': sec_par,
                         'Час виконання: ДД/ММ/РР Год/Хв/Сек': time_func().strftime("  %d.%m.%y %H:%M:%S")})


def time_func():
    print(type((datetime.now()).strftime("%d.%m.%y %H:%M:%S")))
    return datetime.now()


# TIME FORMAT - str - strftime("%d.%m.%y %H:%M:%S")

def strfdelta(tdelta, fmt="{days} дн. {hours} год. {minutes} хв {seconds} сек."):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


@dp.message_handler(commands=['set_time_up'], content_types=['text'])
async def set_time_up(message):
    print("before set_time")
    global time_for_up
    message.text = str(message.text).split(" ")[1]
    if 0 < int(message.text) <= 1440:
        time_for_up = int(message.text) * 60
        print("set time - " + str(time_for_up))
        await bot.send_message(message.chat.id, "Встановлено затримку між виводом UP_SITE повідомлень - " + str(
            int(time_for_up / 60)) + " хв.")
        await logger_writer(first_par="Встановлено затримку між виводом UP_SITE повідомлень - " + str(
            int(time_for_up / 60)) + " хв.", sec_par=" функція : set_time_up")
    else:
        await bot.send_message(message.chat.id, "Недопустиме значення, значення може бути від 0 до 1440 хв(доба)")
        await logger_writer(first_par="Недопустиме значення: " + message.text +
                                      ", значення може бути від 0 до 1440 хв(доба)", sec_par=" функція set_time_up")




@dp.message_handler(commands=['set_time_ssl'], content_types=['text'])
async def set_time_ssl(message):
    print("before set_time")
    global time_for_ssl
    message.text = str(message.text).split(" ")[1]
    if 0 < int(message.text) <= 1440:
        time_for_ssl = int(message.text) * 60
        print("set time - " + str(time_for_ssl))
        await bot.send_message(message.chat.id, "Встановлено затримку між виводом SSL повідомлень - " + str(
            int(time_for_ssl / 60)) + " хв.")
        await logger_writer(first_par="Встановлено затримку між виводом SSL повідомлень - ", sec_par=str(
            int(time_for_ssl / 60)) + " хв. функція : set_time_ssl")

    else:
        await bot.send_message(message.chat.id, "Недопустиме значення, значення може бути від 0 до 1440 хв("
                                                "доба)")
        await logger_writer(first_par="Недопустиме значення: " + message.text +
                                      ", значення може бути від 0 до 1440 хв(доба)", sec_par=" функція set_time_ssl")


@dp.message_handler(commands=['stop_ssl_check_nacp'])
async def stop_ssl_check_nacp(message):
    global WhileLoopFlag
    WhileLoopFlag = False
    await bot.send_message(message.chat.id, text="Зупиняємо процес перевірки SSL")
    await logger_writer(first_par="Зупиняємо процес перевірки ", sec_par=' функція: stop_ssl_check_nacp')


@dp.message_handler(commands=['stop_up_nacp'])
async def stop_up_nacp(message: types.Message):
    global WhileLoopFlag_nacp
    WhileLoopFlag_nacp = False

    await bot.send_message(message.chat.id, text="Зупиняємо процес перевірки ")
    await logger_writer(first_par="Зупиняємо процес перевірки ", sec_par='функцція: stop_up_nacp')


@dp.message_handler(commands=['up_nacp'])
async def up_nacp(message):
    global nacp_sites
    global time_for_up
    global down_time
    three_times_errors = config.times_errors
    await bot.send_message(message.chat.id,
                           "Запускаємо перевірку UP_SITE (1 раз на " + str(int(time_for_up) / 60) + " хв)")
    await logger_writer(first_par="Запускаємо перевірку UP_SITE ",
                        sec_par="(1 раз на " + str(int(time_for_up) / 60) + " хв)")

    global WhileLoopFlag_nacp
    WhileLoopFlag_nacp = True
    while WhileLoopFlag_nacp is True:
        output = ""

        try:
            for key in nacp_sites:
                print(key)
                try:
                    hostname = key.split('/')[2]
                except IndexError:
                    HOST = str(key).split(":")
                    print(HOST)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((HOST[0], int(HOST[1])))
                    if result == 0:
                        if nacp_sites[key] is False:
                            nacp_sites[key] = True
                            deltatime = datetime.now() - down_time[key]
                            await bot.send_message(message.chat.id, "RECOVERY: 🟢\n" + str(key) + "\n" +
                                                   "Up since: " + time_func().strftime("%d.%m.%y %H:%M:%S") + "\n" +
                                                   "Був вимкнений протягом "
                                                   + strfdelta(deltatime))
                            await logger_writer(first_par=str(key),
                                                sec_par="RECOVERY: 🟢 Був вимкнений протягом: "
                                                        + strfdelta(deltatime))
                        print("Port is open")
                    else:
                        three_times_errors[key] += 1
                        if nacp_sites[key] is True:
                            down_time[key] = time_func()
                            if three_times_errors[key] == config.n_times_clause:
                                nacp_sites[key] = False
                                await bot.send_message(message.chat.id, "ALERT: DOWN 🛑\n" +
                                                       str(key) + "\nDown since: " +
                                                       str(down_time[key].strftime("%d.%m.%y %H:%M:%S"))
                                                       + "\nReason: нема відповідді від сервера")
                                await logger_writer(first_par=str(key),
                                                    sec_par="ALERT: DOWN 🛑 Down since:  "
                                                            + str(down_time[key].strftime("%d.%m.%y %H:%M:%S   ")))
                                three_times_errors[key] = 0
                        print("Port is not open")
                    sock.close()
                    continue

                try:
                    async with aiohttp.ClientSession() as session:

                        try:
                            #TIMEOUT - 10 SEС
                            async with session.get(url=key, timeout=10) as response:
                                print(str(response.status) + " " + hostname)
                                if response.status != 200 and response.status != 401:
                                    output += (hostname + "  status_code: " + str(response.status) + " FAIL\n")
                                    if nacp_sites[key] is True:
                                        nacp_sites[key] = False
                                        down_time[key] = time_func()
                                        await bot.send_message(message.chat.id, "ALERT: DOWN 🛑\n" +
                                                               hostname + "\nDown since: " +
                                                               str(down_time[key].strftime("%d.%m.%y %H:%M:%S"))
                                                               + "\nReason: з'єднання з сервером встановлено, "
                                                                 "але отримано error.\n Помилка: " +
                                                               (str(response.status)))
                                        await logger_writer(first_par=hostname,
                                                            sec_par="ALERT: DOWN 🛑 Down since:  "
                                                            + str(down_time[key].strftime("%d.%m.%y %H:%M:%S   ")))

                                elif response.status == 200 or response.status == 401:
                                    if nacp_sites[key] is False:
                                        nacp_sites[key] = True
                                        deltatime = datetime.now() - down_time[key]
                                        await bot.send_message(message.chat.id,
                                                               "RECOVERY: 🟢\n" + hostname + "\nUp since: "
                                                               + time_func().strftime("%d.%m.%y %H:%M:%S") + "\n" +
                                                               "Був вимкнений протягом "
                                                               + strfdelta(deltatime))
                                        await logger_writer(first_par=hostname,
                                                            sec_par="RECOVERY: 🟢 Був вимкнений протягом: "
                                                                    + strfdelta(deltatime))

                        except asyncio.TimeoutError:
                            three_times_errors[key] += 1
                            if nacp_sites[key] is True:
                                down_time[key] = time_func()
                                if three_times_errors[key] == config.n_times_clause:
                                    nacp_sites[key] = False
                                    await bot.send_message(message.chat.id,
                                                           "ALERT: DOWN 🛑\n" + hostname +
                                                           "\nReason: Connection Timeout. " + str(three_times_errors[key])
                                                           +" невдалі спроби з'єднання підряд.\nDown since: "
                                                           + str(down_time[key].strftime("%d.%m.%y %H:%M:%S")))
                                    await logger_writer(first_par=hostname,
                                                        sec_par="ALERT: DOWN 🛑 Connection Timeout. Down since: "
                                                                + str(down_time[key].strftime("%d.%m.%y %H:%M:%S   ")))
                                    three_times_errors[key] = 0

                            if (hostname + "  timeout fail \n") is not output:
                                output += (hostname + "  timeout fail \n")
                                print(output)
                except OSError:
                    three_times_errors[key] += 1
                    print(hostname + " OSError")
                    if nacp_sites[key] is True:
                        down_time[key] = time_func()
                        if three_times_errors[key] == config.n_times_clause:
                            nacp_sites[key] = False
                            await bot.send_message(message.chat.id,
                                                   "ALERT: DOWN 🛑\n" + hostname +
                                                   "\nReason: OSError. " + str(three_times_errors[key])
                                                           +" невдалі спроби з'єднання підряд. \nDown since: " + str(
                                                       down_time[key].strftime("%d.%m.%y %H:%M:%S")) +
                                                   "\n(нема відповіді від сервера)")
                            await logger_writer(first_par=hostname, sec_par="ALERT: DOWN 🛑 OSError. Down since: " + str(
                                down_time[key].strftime("%d.%m.%y %H:%M:%S   ")))
                            three_times_errors[key] = 0


                            print(str(response.status) + "RESPONSE OSE EROOR STATUS")

        except TypeError:
            print(" TypeError")
        await asyncio.sleep(time_for_up)
    print(nacp_sites)
    await bot.send_message(message.chat.id, text="Перевірка UP_SITE зупинена")
    await logger_writer(first_par="Перевірка UP_SITE зупинена", sec_par=" функція up_nacp")


@dp.message_handler(commands=['ssl_check_nacp'])
async def ssl_check_nacp(message):
    global time_for_ssl
    await bot.send_message(message.chat.id,
                           "Запускаємо перевірку SSL-сертифікатів (1 раз на " + str(int(time_for_ssl) / 60) + " хв)")
    await logger_writer(
        first_par="Запускаємо перевірку SSL-сертифікатів (1 раз на " + str(int(time_for_ssl) / 60) + " хв)",
        sec_par=" функція ssl_check_nacp")

    global nacp_sites_ssl
    global WhileLoopFlag
    WhileLoopFlag = True
    while WhileLoopFlag is True:
        out = ""
        try:
            for x in nacp_sites_ssl:
                hostname = x.split('/')[2]

                try:
                    async with aiohttp.ClientSession() as session:
                        try:
                            ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
                            context = ssl.create_default_context()
                            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname, )
                            # TIMEOUT WAS 3.0
                            conn.settimeout(3.0)
                            conn.connect((hostname, 443))
                            ssl_info = conn.getpeercert()
                            Exp_ON = datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
                            Days_Remaining = Exp_ON - datetime.utcnow()
                            conn.close()
                            daysR = int(str(Days_Remaining).split(" ")[0])
                            if daysR <= 40:
                                out += (hostname + " " + str(daysR) + " 🛑\n")
                            else:
                                out += (hostname + " " + str(daysR) + " 🟢\n")

                        except asyncio.TimeoutError:
                            out += hostname + " - TIMEOUT FAIL\n"
                            print(out)
                            await logger_writer(first_par=hostname + " - TIMEOUT FAIL",
                                                sec_par=" функція ssl_check_nacp")
                except OSError:

                    out += hostname + " - OSErorr\n"
                    print(out)
                    await logger_writer(first_par=hostname + " - OSErorr", sec_par=" функція ssl_check_nacp")
        except TypeError:
            print("TypeError")
        await bot.send_message(message.chat.id, out)
        await asyncio.sleep(time_for_ssl)

    await bot.send_message(message.chat.id, text="Перевірка SSL зупинена")
    await logger_writer(first_par="Перевірка SSL зупинена", sec_par=" функція ssl_check_nacp")


@dp.message_handler(commands=["help"])
async def help(message):
    await bot.send_message(message.chat.id,
                           "/set_time_up N, де N - час в хвилинах який вказує відрізок часу між перевірками доступу "
                           "до сайту (default - 1).\n\n "
                           " ПОТРІБНО ПРОПИСУВАТИ ВРУЧНУ, наприклад   '/set_time_up 50'   - перевірка буде кожних 50хв "
                           "(значення може бути від 1 до 1440хв(24години).\n\n"
                           "/set_time_ssl N, де N - час в хвилинах який вказує відрізок часу між перевірками SSL ("
                           "default - 1).\n\n "
                           " ПОТРІБНО ПРОПИСУВАТИ ВРУЧНУ, наприклад   '/set_time_up 50'   - перевірка буде кожних 50хв "
                           "(значення може бути від 1 до 1440хв(24години).\n\n"
                           "/up_nacp - почати перевірку доступності сайтів кожних N хвилин.\n\n"
                           "/ssl_check_nacp - почати перевірку SSL кожних N хвилин.\n\n"
                           "/stop_ssl_check_nacp - зупинити первірку SSL.\n\n"
                           "/stop_up_nacp - зупинити перевірку доступності сайтів.\n\n"
                           )
    await logger_writer(first_par="help повідомлення в чат", sec_par=" функція help")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
