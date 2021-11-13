import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from database import cache
import logging
from environs import Env
from questions import questions
import re
from questions_functions import (
    get_next_question,
    get_cleaned_text,
    get_answer
)


log = logging.getLogger(__name__)


def handle_new_question_request(vk_api, user_id, keyboard):
    user = f'vk-{user_id}'

    question = get_next_question(questions, user)
    user_data = {'question': question}
    cache.hmset(user, user_data)
    vk_api.messages.send(
        user_id=user_id,
        message=question,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )


def give_up(vk_api, user_id, keyboard):
    user = f'vk-{user_id}'
    current_question = cache.hget(user, 'question')
    answer = get_answer(questions, current_question)

    vk_api.messages.send(
        user_id=user_id,
        message=f'Правильный ответ:\n\n{answer}',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )
    question = get_next_question(questions, user)

    user_data = {'question': question}
    cache.hmset(user, user_data)

    vk_api.messages.send(
        user_id=user_id,
        message=question,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )


def handle_solution_attempt(vk_api, user_id, keyboard, event):
    user = f'vk-{user_id}'
    current_question = cache.hget(user, 'question')
    score = cache.hget(user, 'score') or 0

    if current_question:
        answer = get_answer(questions, current_question)
        cleaned_answer = get_cleaned_text(answer)
        cleaned_input = get_cleaned_text(str(event.text))
        pattern = re.compile(cleaned_answer)
        if pattern.match(cleaned_input):
            vk_api.messages.send(
                user_id=user_id,
                message="""Правильно! Поздравляю!
                Для следующего вопроса нажми «Новый вопрос»""",
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            if not 'score':
                score = 1
            else:
                score = int(score) + 1
            user_data = {'question': current_question, 'score': score}
            cache.hmset(user, user_data)
        else:
            vk_api.messages.send(
                user_id=user_id,
                message='Неправильно… Попробуешь ещё раз?',
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
    else:
        vk_api.messages.send(
            user_id=user_id,
            message='Для следующего вопроса нажми «Новый вопрос»',
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard()
        )


def score(vk_api, user_id, keyboard):
    user = f'vk-{user_id}'
    score = cache.hget(user, 'score') or 0
    vk_api.messages.send(
        user_id=user_id,
        message=f'Ваш счёт: {score}',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
        )


def main(vk_token):

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Следующий вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Счёт', color=VkKeyboardColor.SECONDARY)

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            if event.text == 'Начать':
                handle_new_question_request(vk_api, user_id, keyboard)
            elif event.text == 'Следующий вопрос':
                handle_new_question_request(vk_api, user_id, keyboard)
            elif event.text == 'Сдаться':
                give_up(vk_api, user_id, keyboard)
            elif event.text == 'Счёт':
                score(vk_api, user_id, keyboard)
            else:
                handle_solution_attempt(vk_api, user_id, keyboard, event)


if __name__ == '__main__':

    cache.flushdb()

    env = Env()
    env.read_env()

    token = env('VK_TOKEN')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    main(token)
