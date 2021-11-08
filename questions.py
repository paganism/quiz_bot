
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
                questions.append({'question': question, 'answer': answer})
    return questions


questions = read_file('quiz-questions/120br.txt')

