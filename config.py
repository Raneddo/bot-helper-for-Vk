from datetime import datetime

me = 1337 # some number
app_id = 1337 # some number
group_id = 1337 # some number
METHODS_LIST = {'meme', 'meet', 'age', 'friends', 'help'}

token = 'token'  # @liprv

bot_token = 'bot token (group token)'


MAYBE_ERROR = 'Вероятно, вы допустили какую-то ошибку. ' \
              'Но, я проверю логи и пойму, если ошибка у меня.'


def log_to_file(filename: str, message: str):
    with open(filename, 'a') as f:
        if type(message) == str:
            f.write(message + ' ' + datetime.today().__str__() + '\n')
        else:
            f.write('Сообщение с ошибкой' + datetime.today().__str__() + '\n')
