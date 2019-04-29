from random import randint


def reply(bot_api, event, message='<Message>'):
    """
    Function for fast replying
    """
    bot_api.messages.send(user_id=event.object.peer_id,
                          message=message,
                          random_id=randint(0, 9999999999))
