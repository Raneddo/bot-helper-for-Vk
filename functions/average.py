from datetime import datetime

from vk_api import vk_api


from . import help, messages
import config


def average(self, event, options):
    """
    Get age of person from average(friends@.age)
    """
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

        user_id = response[0]['id']
        ans = get_aver_age(self, user_id)
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
        e = e.__str__()
        self.session.RPS_DELAY = 1
        config.log_to_file('out_sorry.log', 'error ' + e)
        messages.reply(self.bot_api, event,
                       message='К сожалению, возникли неполадки. '
                               'Скоро постараюсь всё восстановить.'
                               '\nКроме того, советую проверить правильность '
                               'введёных данных, '
                               'а также то, что у пользователя '
                               'друзья открыты для всех пользователей'
                       )


def get_aver_age(self, user_id):
    friends = self.api.friends.get(user_id=user_id, fields=['bdate'])
    friends = [user.get('bdate') for user in friends['items']
               if user.get('bdate') is not None and user['bdate'].count('.') > 1]
    ages = []
    for bdate in friends:
        given_day, given_month, given_year = list(map(int, bdate.split('.')))
        ages.append((datetime.now() - datetime(given_year, given_month, given_day)).total_seconds())
    if len(ages) < 1:
        return "Нет друзей с открытой датой рождения"

    avg_timestamp = sum(ages) / len(ages)
    median = sorted(ages)[len(ages) // 2] / 3600 / 24 / 365
    ans = avg_timestamp / 3600 / 24 / 365
    return str(ans) + ' точный средний возраст друзей\n' + \
                      str(median) + ' медианный возраст\n' + \
                      str(int((3 * median + ans) // 4)) + ' приблизительно лет'
