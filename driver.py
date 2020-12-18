from scripts.question_generator import Article

import json

def generate_trivia():

    TOPICS_FILE = open('./topics.txt')
    QUESTIONS_FILE = open('./questions.txt', 'w')

    questions = []

    for article in TOPICS_FILE:
        article = Article(title=article)
        questions = questions + article.generate_trivia_sentences()

    # Output JSON
    QUESTIONS_FILE.write(json.dumps(questions, sort_keys=True, indent=4))

    TOPICS_FILE.close()
    QUESTIONS_FILE.close()


if __name__ == '__main__':
    generate_trivia()
