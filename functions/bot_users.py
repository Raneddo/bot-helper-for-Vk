from random import randint
from . import messages


def get_users_list(self, users: list) -> list:
    """
    Generate links with name from id
    """
    users_list = []
    for pack in users:
        temp = self.api.users.get(user_ids=pack)
        users_list += ['[id{0}|{1} {2}]'.format(x['id'], x['first_name'], x['last_name']) for x in temp]
    if len(users_list) < 1:
        users_list = ['Таких пользователей нет']
    return users_list


def broadcast(self, options: str) -> None:
    """
    Function for send message for all active users
    """
    users = self.db.get_active()
    users = [str(x[0]) for x in users]
    users = [','.join(users[i:i + 100]) for i in range((len(users) - 1) // 100 + 1)]
    for pack in users:
        self.bot_api.messages.send(
            user_ids=pack,
            message=options,
            random_id=randint(0, 9999999999)
        )


def all_users(self, event) -> None:
    """
    Get all users from database
    """
    users = self.db.get_all()
    users = [str(x[0]) for x in users]
    users = [','.join(users[i:i + 5000]) for i in range((len(users) - 1) // 5000 + 1)]
    users_list = get_users_list(self, users)
    messages.reply(self.bot_api, event, message='\n'.join(users_list))


def active(self, event) -> None:
    """
    Get only active (with allow messages) users from database
    """
    users = self.db.get_active()
    users = [str(x[0]) for x in users]
    users = [','.join(users[i:i + 5000]) for i in range((len(users) - 1) // 5000 + 1)]
    users_list = get_users_list(self, users)
    messages.reply(self.bot_api, event, message='\n'.join(users_list))


def fuckers(self, event) -> None:
    """
    Get only deactivated (with deny messages) users from database
    """
    users = self.db.get_deactivated()
    users = [str(x[0]) for x in users]
    users = [','.join(users[i:i + 5000]) for i in range((len(users) - 1) // 5000 + 1)]
    users_list = get_users_list(self, users)
    messages.reply(self.bot_api, event, message='\n'.join(users_list))
