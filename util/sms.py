# /usr/bin/python3
# -*- coding: utf-8 -*-

import pyotp
import urllib
from time import localtime, strftime

import urllib.request
import json
import threading

totp = pyotp.TOTP('base32secret3232',interval=60)
totp_generate = False

def send_sms(phones, text, total_price=0):
    login = '*****'
    password = '*****'
    sender = 'SMSC.RU'
    errors = {
        1: 'Ошибка в параметрах.',
        2: 'Неверный логин или пароль.',
        3: 'Недостаточно средств на счете Клиента.',
        4: 'IP-адрес временно заблокирован из-за частых ошибок в запросах. Подробнее',
        5: 'Неверный формат даты.',
        6: 'Сообщение запрещено (по тексту или по имени отправителя).',
        7: 'Неверный формат номера телефона.',
        8: 'Сообщение на указанный номер не может быть доставлено.',
        9: 'Отправка более одного одинакового запроса на передачу SMS-сообщения либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты. '
    }
    url = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&sender=%s&fmt=3" % (login, password, phones, text, total_price, sender)
    answer = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    return answer

def send_otp(phone,message):
    global totp
    global totp_generate
    lock = threading.Lock()
    with lock:
        if totp_generate is False:
            print(message)
            print(totp.now())
            text_message = message + str(totp.now())
            text_message = strftime("%d.%m.%y %H:%M ", localtime()) + text_message
            answer = send_sms(phone,text_message)
            if "error_code" in answer:
                return False
            totp_generate = not totp_generate
            return True
        else:
            return False

def check_otp(password):
    global totp
    global totp_generate
    lock = threading.Lock()
    with lock:
        if totp_generate is True:
            answer = totp.verify(password)
            totp_generate = not totp_generate
            return answer
        else:
            return None
