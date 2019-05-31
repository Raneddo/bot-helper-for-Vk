#!/usr/bin/env python3

import datetime
import vk_api
import time
import config
# from vk_api.longpoll import VkLongPoll, VkEventType
# from random import randint


session = vk_api.VkApi(app_id=config.app_id,
                       token=config.token)
session.RPS_DELAY = 1
api = session.get_api()


def get_old():
    """
    :return: Getting time from file
    """
    with open('status.txt') as f:
        timer = f.readline()
        old_status = f.read()

    return datetime.datetime.fromtimestamp(int(timer)), old_status


def days_str(count):
    words = [' дней ', ' дня ', ' день ']
    return to_str(count, words)


def hours_str(count):
    words = [' часов ', ' часа ', ' час ']
    return to_str(count, words)


def minutes_str(count):
    words = [' минут ', ' минуты ', ' минута ']
    return to_str(count, words)


def to_str(count, words):
    """
    :return: russian case for given count of time and cases of required word
    """
    if 10 < count < 20 or count % 10 > 4 or count % 10 == 0:
        return words[0]
    if 1 < count % 10 < 5:
        return words[1]
    return words[2]


while True:
    now = datetime.datetime.now()

    delta, text = get_old()
    delta = delta - now
    hours = delta.seconds // 3600
    minutes = delta.seconds % 3600 // 60

    ans = ''
    old = api.status.get()

    if delta.days < 0:
        if text is not None and old != text:
            ans = text
            api.status.set(text=ans)
        time.sleep(60)
        continue
    
    if delta.days > 0:
        ans += str(delta.days) + days_str(delta.days)
    if hours > 0:
        ans += str(hours) + hours_str(hours)
    if minutes > 0:
        ans += str(minutes) + minutes_str(minutes)

    if text is not None and ans:
        ans += ' | ' + text
    elif text is not None:
        ans = text

    if old != text:
        api.status.set(text=ans)
    time.sleep(60)
