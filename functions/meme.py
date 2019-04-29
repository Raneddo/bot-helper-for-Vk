from random import randint
from . import messages


def meme(self, event, options):
    """
    Get first (or picked) or random post from main user's news
    """
    if options is not None:
        if options == 'rand':
            options = randint(1, 1000)
        try:
            options = int(options)
        except ValueError:
            messages.reply(self.bot_api, event, message='Вы ввели не число')
            return

    if options is None:
        options = 1
    new = self.api.newsfeed.get(filters=['post'], count=1,
                                source_ids=['pages'], start_from=options)
    if len(new.get('items')) == 0:
        messages.reply(self.bot_api, event, message='Произошла ошибка. Нет записей.')
        return
    post_id = new['items'][0]['post_id']
    source_id = new['items'][0]['source_id']
    self.bot_api.messages.send(user_id=event.object.peer_id,
                               attachment=('wall' + str(source_id) + '_' + str(post_id)),
                               random_id=randint(0, 9999999999))
