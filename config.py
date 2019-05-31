from datetime import datetime

me = 135554479
app_id = 5909741
group_id = 177021512
METHODS_LIST = {'meme', 'meet', 'age', 'friends', 'help'}

token = 'token must be here'

password = 'pass must be here'

bot_token = 'token must be here'

MAYBE_ERROR = 'Вероятно, вы допустили какую-то ошибку. ' \
              'Но, я проверю логи и пойму, если ошибка у меня.'


def log_to_file(filename: str, message: str):
    with open(filename, 'a') as f:
        if type(message) == str:
            f.write(message + ' ' + datetime.today().__str__() + '\n')
        else:
            f.write('Сообщение с ошибкой' + datetime.today().__str__() + '\n')
