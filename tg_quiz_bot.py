from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from environs import Env


log = logging.getLogger(__name__)


def read_file(filepath):
    questions = []
    with open(filepath, 'r', encoding='koi8-r') as file:
        questions_list = file.read().split('\n\n')
        question = ''
        answer = ''
        for item in questions_list:
            if item.startswith('Вопрос'):
                question = item
            if item.startswith('Ответ'):
                answer = item
                questions.append({question: answer})
    return questions


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    log.warning('Update "%s" caused error "%s"', update, error)


def main(token):
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # print(read_file('quiz-questions/120br.txt'))

    env = Env()
    env.read_env()

    token = env('TELEGRAM_TOKEN')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    main(token)
