import config
from . import messages


def meet(self, event):
    """
    Get random user from VK who was online last 2 weeks
    """
    try:
        if len(self.people) < 1:
            messages.reply(self.bot_api, event,
                           message='Пользователей в списке нет. '
                                   'Попробуйте через несколько минут.')
        else:
            messages.reply(self.bot_api, event,
                           message='I think @id' + str(self.people[-1]) + "(this person) is cool")
            self.people.pop(-1)

    except Exception as e:
        e = e.__str__()
        config.log_to_file('out_sorry.log', 'error ' + e)
        messages.reply(self.bot_api, event,
                       message='К сожалению, возникли неполадки. '
                               'Скоро постараюсь всё восстановить.')
