from . import messages


def help_meet():
    return ("Всё предельно просто. Всего одна команда.\n"
            "/meet"
            )


def help_meme():
    return ("Теперь можно ввести число n, и вам покажется n-ый мем из списка "
            "новостей бота.\n\n"
            "А если вы введёте `rand`, то вам выпадет случайный мем, "
            "но предупреждаю, он может быть бабаяном!\n\n"
            "Также вы можете предложить хороший паблик в лс @liprv(Роману)\n"
            "\n"
            "Примеры запросов:\n"
            "/meme -- первый пост\n"
            "/meme 2 -- второй (n-ный пост)\n"
            "/meme rand -- случайный пост"
            )


def help_help():
    return "Любишь рекурсию?"


def help_age():
    return ("С помощью этой функции вы можете узнать скрытый возраст человека вк\n"
            "\n"
            "Примеры запросов:\n"
            "/age vk.com/liprv\n"
            "/age liprv\n"
            "/age id1234567\n"
            "/age vk.com/id1234567"
            )


def help_friends():
    return ("С помощью этой функции вы можете узнать общих друзей 2-5 пользователей\n"
            "(Паблики нет смысла отправлять, работать не будет. "
            "Некорректные ссылки игнорируются)\n"
            "\n"
            "Примеры запросов:\n"
            "/friends vk.com/liprv vk.com/kek\n"
            "/friends vk.com/liprv kek\n"
            "/friends liprv kek id1 id123456\n"
            "/friends vk.com/id404 vk.com/id555 liprv\n"
            "\n"
            "Вы можете отправлять ссылки через "
            "пробел или перенос строки."
            )


def help_invalid():
    """
    :return: string for if picked function is not available
    """
    return ("Такой функции не существует. "
            "Введите функцию из списка\n"
            "/help")


def get_help_func(name: str):
    """
    Getting function of help from name
    """
    functions = {
        'meet': help_meet,
        'meme': help_meme,
        'age': help_age,
        'help': help_help,
        'friends': help_friends,
    }
    return functions.get(name, help_invalid)


def main_help(self, event, options):
    """
    Function for pick help page
    """
    if options is None:
        messages.reply(self.bot_api, event,
                       message="'/help' ‒ Это сообщение.\n"
                               "\n"
                               "'/meet' ‒ Ссылка на случайную страницу.\n"
                               "\n"
                               "'/meme' ‒ Запись в моих новостях из пабликов (По умолчанию первая).\n"
                               "\n"
                               "'/age' ‒ Узнать скрытый возраст человека\n"
                               "\n"
                               "'/friends' ‒ Узнать общих друзей 2-5 пользователей\n"
                               "\n"
                               "Вы можете узнать подробнее о функциях, введя\n"
                               "/help <func name> без <>)\n"
                               "Перед использоваеним функция, рекомендую ознакомиться с их "
                               "страничками /help"
                       )
    else:
        messages.reply(self.bot_api, event, message=get_help_func(options)())
