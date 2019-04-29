from . import help, messages
import config
import vk_api


class User:
    def __init__(self, user_id, fn, ln, public=None, city_id=None):
        self.user_id = user_id
        self.fn = fn
        self.ln = ln
        self.city_id = city_id
        self.public = public


def age(self, event, options) -> None:
    """
    The main function
    """
    if options is None:
        messages.reply(self.bot_api, event, message=help.help_age())
        return
    try:
        options = options.split('/')[-1]
        response = self.api.users.get(user_ids=[options])
        if len(response) < 1:
            messages.reply(self.bot_api, event,
                           message="Такого пользователя не существует. "
                                   "Проверьте правильность ввода.")
            return
        if response[0].get('can_access_closed') is False:
            messages.reply(self.bot_api, event,
                           message="К сожалению, пользователь закрыл профиль, и "
                                   "теперь невозможно найти возраст.")
            return

        options = response[0]['id']
        ans = get_age(self, options)
        self.session.RPS_DELAY = 1
        messages.reply(self.bot_api, event, message=str(ans))
    except vk_api.ApiError as e:
        self.session.RPS_DELAY = 1
        if e.code == 113:
            messages.reply(self.bot_api, event,
                           message="Такого пользователя не существует. "
                                   "Проверьте правильность ввода.")
            return
        e = e.__str__()
        config.log_to_file('out_sorry.log', 'error ' + e)
        messages.reply(self.bot_api, event, message=config.MAYBE_ERROR)

    except Exception as e:
        self.session.RPS_DELAY = 1
        e = e.__str__()
        config.log_to_file('out_sorry.log', 'error ' + e)
        messages.reply(self.bot_api, event, message=config.MAYBE_ERROR)


def get_by_city(self, user: User) -> str:
    left = 13
    right = 115
    while right - left > 1:
        m = (left + right) // 2
        users = self.api.users.search(q=(user.fn + ' ' + user.ln), sort=1, count=1000, city=user.city_id,
                                      age_from=left, age_to=m)['items']
        users = [int(x['id']) for x in users]
        if user.user_id in users:
            right = m
        else:
            left = m
    users = self.api.users.search(q=(user.fn + ' ' + user.ln), sort=1, count=1000, city=user.city_id,
                                  age_from=left, age_to=left)['items']
    users = [int(x['id']) for x in users]
    if user.user_id not in users:
        left += 1
    if left > 114:
        return ("К сожалению, данный пользователь "
                "не просто скрыл возраст, а даже "
                "не указал его, и теперь узнать вы можете "
                "лишь написав лично.\n"
                )
    return str(left) + ' лет'


def get_by_public(self, user: User) -> str:
    left = 13
    right = 115

    while right - left > 1:
        m = (left + right) // 2
        users = self.api.users.search(q=(user.fn + ' ' + user.ln), sort=1, count=1000, group_id=user.public,
                                      age_from=left, age_to=m)['items']
        users = [int(x['id']) for x in users]
        if user.user_id in users:
            right = m
        else:
            left = m
    users = self.api.users.search(q=(user.fn + ' ' + user.ln), sort=1, count=1000, group_id=user.public,
                                  age_from=left, age_to=left)['items']
    users = [int(x['id']) for x in users]
    if user.user_id not in users:
        left += 1
    if left > 114:
        return ("К сожалению, данный пользователь "
                "не просто скрыл возраст, а даже "
                "не указал его, и теперь узнать вы можете "
                "лишь написав лично.\n"
                )
    return str(left) + ' лет'


def get_age(self, user_id: int) -> str:
    """
    :return age of entered human or string about 
    """
    self.session.RPS_DELAY = 0.23
    user = self.api.users.get(user_ids=[user_id], fields=['city'])[0]
    fn = user['first_name']
    ln = user['last_name']
    city_id = user.get('city')
    public = self.api.users.getSubscriptions(user_id=user_id)['groups']
    user = User(user_id, fn, ln)
    if public['count'] > 1:
        user.public = int(public['items'][-1])
        return get_by_public(self, user)

    elif city_id is not None:
        user.city_id = int(city_id['id'])
        return get_by_city(self, user)
    else:
        return "К сожалению, не могу дать вам ответа, так как у человека не указан город, " \
               "без которого нагрузка на сервер сильно возрастает и вк блокирует запросы"
