from scripts.utils import get_topic_list
from scripts.scraper import scrape_topics
from scripts.text_processing import summarize_text
from scripts.mcq_generator import MCQ_Generator

# import nltk

# nltk.download('stopwords')
# nltk.download('popular')


def generate_quiz():
    topic_list = get_topic_list()
    scrape_topics(topic_list)
    # summarize_text(topic_list)

    question_list = []

    for filename in topic_list.values():
        topic_file = open('./scraped_pages/' + filename +
                          '.txt', 'r', encoding='utf-8')
        summary_file = open('./scraped_pages/' + filename +
                            '_summarised.txt', 'r', encoding='utf-8')
        topic_text = topic_file.read()
        summary_text = summary_file.read()

        generator = MCQ_Generator(topic_text, topic_text)
        question_list += generator.get_MCQs()
        topic_file.close()
        summary_file.close()

    for item in question_list:
        print(item)


if __name__ == '__main__':
    generate_quiz()
