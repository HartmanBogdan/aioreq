time_for_up = 60  # час в секундах - це затрамка між перевірками доступності сайтів - за замовчуванням - 1 хв
time_for_ssl = 86400  # час в секундах - це затримка між перевірками SSL сертифікатів, за замовчуванняи - 24години
# (60секунд * 60хв *24години = 86400секунд в 24годинах)
WhileLoopFlag = True  # це флаг, який дає дозвіл(або заборону) на безперервну перевірку сертифікатів,
# за замовчуванням - True,
# змінюється лише в функції stop_ssl_check_nacp() = False та в ssl_check_nacp() = True в файлі main.py
WhileLoopFlag_nacp = True  # це флаг, який, який дає дозвіл(або заборону) на безперервну перевірку доступності сайтів,
# за замовчуванням - True, змінюється лише в функції stop_up_nacp() = False та в up_nacp() = True в файлі main.py

nacp_sites = {  # СПИСОК САЙТІВ, В ЯКИХ ПОТРІБНО ПЕРЕВІРЯТИ ДОСТУПНІСТЬ
    'https://interes.shtab.net/': True,
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
    'https://acskidd.gov.ua/': True
}

nacp_sites_ssl = {  # СПИСОК САЙТІВ, В ЯКИХ ПОТРІБНО ПЕРЕВІРЯТИ СЕРТИФІКАТ ССЛ
    'https://interes.shtab.net/': True,
    'https://sanctions.nazk.gov.ua/': True,
    'https://vision.nazk.gov.ua/': True,
    'https://prosvita.nazk.gov.ua/': True,
    'https://antycorportal.nazk.gov.ua/': True,
    'https://study.nazk.gov.ua/': True,
    'https://wiki.nazk.gov.ua/': True,
    'https://nazk.gov.ua/uk/': True,
    # 'https://erp.nazk.gov.ua/': True,
    'https://jira.nazk.gov.ua/': True,
    # 'https://confluence.nazk.gov.ua/': True,
    'https://cloud.nazk.gov.ua': True,
    'https://nacpworkspace.slack.com/': True
}
