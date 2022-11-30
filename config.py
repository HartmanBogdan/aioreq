"""
set_time_up - таймер для мон.сайтів, вказувати в ХВИЛИНАХ. див. help
set_time_ssl - таймер для SSL сертф, вказувати в ХВИЛИНАХ.  див. help
up_nacp - почати моніторинг сайтів
ssl_check_nacp - почати моніторинг ssl
stop_ssl_check_nacp - зупинити моніторинг ssl
stop_up_nacp - зупинити моніторинг сайтів
help - пояснення для таймерів
"""

API_TOKEN = '5521564357:AAEyEl6zrML9PGMY-vunQesbEU0d4ZWdw1Y'  # ссилка на бот ТОКЕН ПО ЯКОМУ СКРИПТ КОНЕКТИТЬСЯ ДО
# КОНКРЕТНОГО БОТА В ТЕЛЕГРАМІ. Узнать токен можна в телеграмі в https://t.me/BotFather (бот прив'язується до
# конкретного акаунта( номера телефону) 5521564357:AAEyEl6zrML9PGMY-vunQesbEU0d4ZWdw1Y - @check_response_bot -
# основний бот. 5518084108:AAGNt_MEkbPtkvL8GJ_4c1RRgF7DGuVyAE8 - @nazk_up_bot - тестовий бот.


time_for_up = 60  # час в секундах - це затрамка між перевірками доступності сайтів - за замовчуванням - 1 хв
time_for_ssl = 86400  # час в секундах - це затримка між перевірками SSL сертифікатів, за замовчуванняи - 24години
# (60секунд * 60хв *24години = 86400секунд в 24годинах)
WhileLoopFlag = True  # це флаг, який дає дозвіл(або заборону) на безперервну перевірку сертифікатів,
# за замовчуванням - True,
# змінюється лише в функції stop_ssl_check_nacp() = False та в ssl_check_nacp() = True в файлі main.py
WhileLoopFlag_nacp = True  # це флаг, який, який дає дозвіл(або заборону) на безперервну перевірку доступності сайтів,
# за замовчуванням - True, змінюється лише в функції stop_up_nacp() = False та в up_nacp() = True в файлі main.py

nacp_sites = {  # СПИСОК САЙТІВ, В ЯКИХ ПОТРІБНО ПЕРЕВІРЯТИ ДОСТУПНІСТЬ
    'https://interes.shtab.net/': True,  # флаг True - показує доступність ресурсу, ДЕФОЛТНО - True, якщо ресурс під час
    # перевірки стає недоступний - флаг стає False, при цьому в окремий dict(ключ : значення)
    # записується сам ресурс(ключ) та дата, коли ресурс перестав бути доступний(значення) - це все в фунеції up_nacp
    'https://sanctions.nazk.gov.ua/': True,
    'https://vision.nazk.gov.ua/': True,
    'https://prosvita.nazk.gov.ua/': True,
    'https://antycorportal.nazk.gov.ua/': True,
    'https://study.nazk.gov.ua/': True,
    'https://wiki.nazk.gov.ua/': True,
    'https://nazk.gov.ua/uk/': True,
    'https://jira.nazk.gov.ua/': True,
    'https://cloud.nazk.gov.ua': True,
    'https://nacpworkspace.slack.com/': True,
    '91.142.175.11:53': True,
    '91.142.175.21:587': True,  # MAIL.NAZK.GOV.UA
    'https://app.slack.com/client/T0140MKGNUU/C013UGADGQ2': True,
    'http://ca.informjust.ua/': True,
    'http://czo.gov.ua': True,
    # 'https://acskidd.gov.ua/': True,  -- з закордону - не моніториться, тільки з України
    'https://corruptinfo.nazk.gov.ua/': True,
    'https://portal.nazk.gov.ua/': True

}

nacp_sites_ssl = [  # СПИСОК САЙТІВ, В ЯКИХ ПОТРІБНО ПЕРЕВІРЯТИ СЕРТИФІКАТ ССЛ
    'https://interes.shtab.net/',
    'https://sanctions.nazk.gov.ua/',
    'https://vision.nazk.gov.ua/',
    'https://prosvita.nazk.gov.ua/',
    'https://antycorportal.nazk.gov.ua/',
    'https://study.nazk.gov.ua/',
    'https://wiki.nazk.gov.ua/',
    'https://nazk.gov.ua/uk/',
    'https://jira.nazk.gov.ua/',
    'https://cloud.nazk.gov.ua',
    'https://nacpworkspace.slack.com/',
    'https://portal.nazk.gov.ua/',
    'https://corruptinfo.nazk.gov.ua/'
]
