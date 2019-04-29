from . import help, messages
import config


def friends(self, event, options):
    """
    Reply all mutual friends of given people
    """
    try:
        if options is None:
            messages.reply(self.bot_api, event, message=help.help_friends())
            return

        options = options.split()
        if len(options) < 2:
            answer = 'Введите ссылки на пользователей, общих друзей которых хотите узнать.\n' \
                     'При этом, между ссылками должен быть ровно один пробел'
            messages.reply(self.bot_api, event, message=answer)

        if len(options) > 5:
            answer = "Ну ёкарный бабай. Совесть имейте. Должны быть же какие-то ограничения..." \
                     "\n(не более 5 пользователей)"
            messages.reply(self.bot_api, event, message=answer)
            return

        for i in range(len(options)):
            options[i] = options[i].split('/')[-1]

        options = list(set(options))

        users = self.api.users.get(user_ids=','.join(options))

        if len(users) < 2:
            messages.reply(self.bot_api, event,
                           message="Введите 2 или более корректные ссылки")
            return

        ans = set()

        user_friends = self.api.friends.get(user_id=users[0]['id'], fields=['name'])['items']
        for fr in user_friends:
            ans.add('[id{0}|{1} {2}]'.format(fr['id'], fr['first_name'], fr['last_name']))

        for i in range(1, len(users)):
            self.session.RPS_DELAY = 0.34
            user_friends = self.api.friends.get(user_id=users[i]['id'], fields=['name'])['items']
            temp = set()
            for fr in user_friends:
                temp.add('[id{0}|{1} {2}]'.format(fr['id'], fr['first_name'], fr['last_name']))
            ans = ans & temp

        self.session.RPS_DELAY = 1

        ans = list(ans)

        if len(ans) < 101:
            answer = '\n'.join(ans)
            if len(ans) < 1:
                answer = ("Вероятно, у данных пользователей нет общих друзей. "
                          "Или хотя бы у одного из них они скрыты.")
            messages.reply(self.bot_api, event, message=answer)
        else:
            for i in range(0, len(ans), 100):
                answer = '\n'.join(ans[i:i + 100])

                messages.reply(self.bot_api, event, message=answer)

    except Exception as e:
        e = e.__str__()
        self.session.RPS_DELAY = 1
        config.log_to_file('out_sorry.log', 'error ' + e)
        messages.reply(self.bot_api, event,
                       message='К сожалению, возникли неполадки. '
                               'Скоро постараюсь всё восстановить.'
                               '\nКроме того, советую проверить правильность '
                               'введёных пользователей, '
                               'а также то, что у каждого из них '
                               'друзья открыты для всех пользователей'
                       )
