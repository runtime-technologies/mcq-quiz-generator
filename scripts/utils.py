def get_topic_list():
    topics_list = {}
    topics_file = open('./topics.txt')

    for topic in topics_file:
        topics_list[topic.strip()] = topic.lower().replace(' ', '_').strip()

    return topics_list

def write_questions_to_file(filename: str, questions: list, question_type: str):
    result = open('./results/' + filename + '_' + question_type +
                  '_questions.txt', 'w', encoding='utf-8')
    
    if(question_type == 'mcq'):
        for question in questions:
            result.write('Q: ' + question['question'] + '\n')
            result.write('A: ' + question['answer'] + '\n')
            options = ', '.join(map(str, question['options']))
            result.write('O: ' + options + '\n\n\n')
    else:
        for question in questions:
            result.write('Q: ' + question + '\n')

    result.close()
