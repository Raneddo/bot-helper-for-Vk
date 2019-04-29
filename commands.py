from random import randint
from time import time
import config
from db_queries import DataBase
from functions import meet, help, age, friends, meme, bot_users, status


class Commands:
    db: DataBase

    def __init__(self, api, longpoll, auto_read, session, bot_api, bot, db):
        self.api = api
        self.bot_api = bot_api
        self.bot = bot
        self.longpoll = longpoll
        self.auto_read = auto_read
        self.session = session
        self.people = []
        self.db = db

    def commands(self, event):
        """
        :command is the word after / but before space or end line
        :options is another text (may be None)

        Function for taking command and call function of picked command with parameter (options)
        """
        text = event.object.text
        text = text.split(maxsplit=1)
        command = text[0]
        options = None
        if len(text) > 1:
            options = text[1]

        if command == '/meet':
            meet.meet(self, event)

        elif command == '/help':
            help.main_help(self, event, options)

        elif command == '/meme':
            meme.meme(self, event, options)

        elif command == '/age':
            age.age(self, event, options)

        elif command == '/friends':
            friends.friends(self, event, options)

        elif event.object.peer_id == config.me:
            if command == '/broadcast':
                bot_users.broadcast(self, options)
            elif command == '/all':
                bot_users.all_users(self, event)
            elif command == '/active':
                bot_users.active(self, event)
            elif command == '/fuckers':
                bot_users.fuckers(self, event)
            elif command == '/status':
                status.status(self, event, options)

    def search_people(self):
        """
        Get 100 random people and take only active users (was online at 2 last weeks)
        """
        self.session.RPS_DELAY = 0.34
        pos = True
        try:
            while pos:
                pos = True
                users = [str(randint(1, 527881663)) for _ in range(100)]
                users = self.api.users.get(user_ids=','.join(users), fields=['last_seen'])
                for user in users:
                    if user.get("deactivated"):
                        continue
                    last_seen = user['last_seen']['time']
                    if time() - last_seen < 604800:
                        self.people.append(user['id'])
                        pos = False
        except Exception as e:
            e = e.__str__()
            config.log_to_file('out_sorry.log', 'error ' + e)
            self.session.RPS_DELAY = 1
