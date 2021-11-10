import random


def get_cleaned_text(text):
    return ''.join(x.lower() for x in text if x.isalpha() or x.isdigit())


def get_next_question(questions, user):
    ind = random.randint(0, len(questions))
    return questions[ind]['question']


def get_answer(questions, question):
    for index, dict_ in enumerate(questions):
        if dict_['question'] == question:
            answer = dict_['answer'].partition("\n")[2]. \
                partition('.')[0].partition('(')[0]
            return answer
