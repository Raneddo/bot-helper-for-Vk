#!/usr/bin/env python3

import sqlite3
from datetime import datetime
from random import randint

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll
# from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import config
# from time import time
from commands import Commands
from db_queries import DataBase

auto_read = False

try:
    database = sqlite3.connect('db.sqlite3')
except sqlite3.Error:
    from generate_database import DataBase
    DataBase()
    database = sqlite3.connect('db.sqlite3')

conn = database.cursor()

db = DataBase(conn, database)


session = vk_api.VkApi(app_id=config.app_id,
                       token=config.token)
session_group = vk_api.VkApi(token=config.bot_token)
session.RPS_DELAY = 1
api = session.get_api()
longpoll = VkLongPoll(session, mode=(2 + 8 + 32 + 64 + 128 + 4096))
bot_api = session_group.get_api()
bot = VkBotLongPoll(vk=session_group, group_id=config.group_id)

print('Bot was started in', datetime.today())
config.log_to_file('out_sorry.log', 'Bot was started in')
bot_api.messages.send(user_id=config.me,
                      message=('Bot was started in ' +
                               datetime.today().__str__()),
                      random_id=randint(0, 999999999))

processing = Commands(api, longpoll, auto_read, session, bot_api, bot, db)

while True:
    try:
        for event in bot.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                db.add_user_to_db(event.object.peer_id)
                if len(event.object.attachments) == 0 and event.object.text[0] == '/':
                    processing.bot_api.messages.setActivity(user_id=event.object.peer_id, type='typing')
                    processing.commands(event)
                if len(processing.people) < 25:
                    processing.search_people()
            elif event.type == VkBotEventType.MESSAGE_ALLOW:

                db.set_is_active(user_id=event.object.user_id)

            elif event.type == VkBotEventType.MESSAGE_DENY:
                db.set_is_not_active(user_id=event.object.user_id)

    except AttributeError as e:
        config.log_to_file('out_sorry.log', str(e))
        print(e, 'AttributeError')

    except ConnectionError as e:
        config.log_to_file('out_sorry.log', str(e))
        session = vk_api.VkApi(app_id=config.app_id,
                               token=config.token)
        processing.api = session.get_api()
        processing.bot_api.messages.send(
            user_id=config.me,
            message="API was updated",
            random_id=randint(0, 9999999999)
        )
    except Exception as e:
        config.log_to_file('out_sorry.log', str(e))
        print(e.args)

        session = vk_api.VkApi(app_id=config.app_id,
                               token=config.token)
        processing.api = session.get_api()
        processing.bot_api.messages.send(
            user_id=config.me,
            message="API was updated. Another error",
            random_id=randint(0, 9999999999)
        )
