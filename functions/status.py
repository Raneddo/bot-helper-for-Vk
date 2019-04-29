import datetime
from . import messages
import config


def status(self, event, options: str):
    """
    Translate date and time from format, save it and reply for success
    """
    try:
        options, text = options.split('\n', maxsplit=1)
        if text is None:
            text = ''
        with open('status.txt', 'w') as f:
            new_time = datetime.datetime.strptime(options, "%d.%m.%y %H:%M")
            f.write(str(int(new_time.timestamp())) + '\n' + text)
            messages.reply(self.bot_api, event, message='Time was updated')
    except Exception as e:
        e = e.__str__()
        messages.reply(self.bot_api, event, message='Something went wrong. Try later.\n'
                                                    'Error: ' + e)
        config.log_to_file('out_sorry.log', 'error ' + e)
