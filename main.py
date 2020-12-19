from scripts.utils import *
from scripts.scraper import scrape_topics
from scripts.text_processing import *

import nltk

nltk.download('stopwords')
nltk.download('popular')


def generate_quiz():
    topic_list = get_topic_list()
    scrape_topics(topic_list)
    


if __name__ == '__main__':
    generate_quiz()
