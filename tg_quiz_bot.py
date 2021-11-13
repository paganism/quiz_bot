from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    ConversationHandler, RegexHandler
)
import logging
from environs import Env
from telegram import ReplyKeyboardMarkup
from questions import questions
from database import cache
import re
from questions_functions import (
    get_next_question,
    get_cleaned_text,
    get_answer
)


log = logging.getLogger(__name__)

NEW_QUESTION, CHECK_ANSWER, GIVE_UP, SCORE = range(4)
CUSTOM_KEYBOARD = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
REPLY_MARKUP = ReplyKeyboardMarkup(CUSTOM_KEYBOARD)


def start(bot, update):
    update.message.reply_text(
        'Привет, я бот для викторин',
        reply_markup=REPLY_MARKUP
    )
    return NEW_QUESTION


def handle_new_question_request(bot, update, user_data):
    user = f'tg-{update.message.chat.id}'

    question = get_next_question(questions, user)
    cache.set(user, question)
    update.message.reply_text(
            question,
            reply_markup=REPLY_MARKUP
        )
    return CHECK_ANSWER


def error(bot, update, error):
    log.warning('Update "%s" caused error "%s"', update, error)


def done():
    return ConversationHandler.END


def give_up(bot, update, user_data):
    user = f'tg-{update.message.chat.id}'
    current_question = cache.get(user)
    answer = get_answer(questions, current_question)

    update.message.reply_text(
        f'Правильный ответ:\n\n{answer}', reply_markup=REPLY_MARKUP
    )

    question = get_next_question(questions, user)
    cache.set(user, question)
    update.message.reply_text(f'{question}', reply_markup=REPLY_MARKUP)

    return CHECK_ANSWER


def handle_solution_attempt(bot, update, user_data):
    user = f'tg-{update.message.chat.id}'
    current_question = cache.get(user)
    answer = get_answer(questions, current_question)

    cleaned_answer = get_cleaned_text(answer)
    cleaned_input = get_cleaned_text(str(update.message.text))

    pattern = re.compile(cleaned_answer)

    pattern = re.compile(answer.lower())
    if pattern.match(cleaned_input):
        update.message.reply_text(
            """Правильно! Поздравляю!
            Для следующего вопроса нажми «Новый вопрос»""",
            reply_markup=REPLY_MARKUP
        )
        if 'score' not in user_data:
            user_data['score'] = 1
        else:
            user_data['score'] += 1
        return NEW_QUESTION
    update.message.reply_text(
            'Неправильно… Попробуешь ещё раз?',
            reply_markup=REPLY_MARKUP
        )
    return CHECK_ANSWER


def score(bot, update, user_data):
    if 'score' not in user_data:
        user_data['score'] = 0
    update.message.reply_text(
        f"Ваш счёт\n\n{user_data['score']}",
        reply_markup=REPLY_MARKUP
    )
    return NEW_QUESTION


def main(token):

    updater = Updater(token)
    dp = updater.dispatcher

    dp.add_error_handler(error)
    conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', start),
                RegexHandler(
                    '^(Новый вопрос)$',
                    handle_new_question_request,
                    pass_user_data=True
                ),
                RegexHandler(
                    '^Сдаться$',
                    give_up,
                    pass_user_data=True
                ),
                RegexHandler(
                    '^(Мой счёт)$',
                    score,
                    pass_user_data=True
                ),
            ],

            states={
                NEW_QUESTION: [
                    RegexHandler(
                        '^(Новый вопрос)$',
                        handle_new_question_request,
                        pass_user_data=True
                    ),
                    RegexHandler(
                        '^Сдаться$',
                        give_up,
                        pass_user_data=True
                    ),
                    RegexHandler(
                        '^(Мой счёт)$',
                        score,
                        pass_user_data=True
                    ),
                ],

                GIVE_UP: [
                    RegexHandler(
                        '^(Мой счёт)$',
                        score,
                        pass_user_data=True
                    ),
                    RegexHandler(
                        '^Сдаться$',
                        give_up,
                        pass_user_data=True
                    ),
                ],
                CHECK_ANSWER: [
                    RegexHandler(
                        '^(Мой счёт)$',
                        score,
                        pass_user_data=True
                    ),
                    RegexHandler(
                        '^Сдаться$',
                        give_up, pass_user_data=True
                    ),
                    MessageHandler(
                        Filters.text,
                        handle_solution_attempt,
                        pass_user_data=True
                    ),
                ],
                SCORE: [
                    RegexHandler('^(Мой счёт)$', score, pass_user_data=True),
                ],
            },

            fallbacks=[
                RegexHandler('^Завершить$', done, pass_user_data=True),
                RegexHandler('^Сдаться$', give_up, pass_user_data=True),
            ]
        )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    cache.flushdb()

    env = Env()
    env.read_env()

    token = env('TELEGRAM_TOKEN')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    main(token)
