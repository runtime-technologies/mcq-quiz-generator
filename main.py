import sys

from scripts.utils import get_topic_list, write_questions_to_file
from scripts.scraper import scrape_topics
from scripts.text_processing import summarize_text

from scripts.mcq_generator import MCQ_Generator
from scripts.whq_generator import WHQ_Generator


def generate_quiz(scrape_topics=True, summarize_topics=False):
    topic_list = get_topic_list()
    if scrape_topics:
        scrape_topics(topic_list)
    if summarize_topics:
        summarize_text(topic_list)

    mcq_question_list = {}
    whq_question_list = {}

    for topic, filename in topic_list.items():
        topic_file = open('./scraped_pages/' + filename +
                          '.txt', 'r', encoding='utf-8')
        topic_text = topic_file.read()

        print('Generating MCQ questions for:', topic)

        if summarize_topics:
            summary_file = open('./scraped_pages/' + filename +
                                '_summarised.txt', 'r', encoding='utf-8')
            summary_text = summary_file.read()
            mcq_generator = MCQ_Generator(topic_text, summary_text)

        else:
            mcq_generator = MCQ_Generator(topic_text, topic_text)

        mcq_generated_questions = mcq_generator.get_MCQs()

        print('Generating WH questions for:', topic)
        whq_generator = WHQ_Generator(topic_text)
        whq_generated_questions = whq_generator.parse(topic_text)

        mcq_question_list[topic] = mcq_generated_questions
        whq_question_list[topic] = whq_generated_questions

        topic_file.close()

        print("Storing questions for:", topic)
        write_questions_to_file(filename, mcq_generated_questions, 'mcq')
        write_questions_to_file(filename, whq_generated_questions, 'whq')


if __name__ == '__main__':
    generate_quiz()
