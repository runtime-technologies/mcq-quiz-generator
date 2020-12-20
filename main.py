from scripts.utils import get_topic_list
from scripts.scraper import scrape_topics
from scripts.text_processing import summarize_text
from scripts.mcq_generator import MCQ_Generator

# import nltk

# nltk.download('stopwords')
# nltk.download('popular')


def generate_quiz():
    topic_list = get_topic_list()
    keyword_dict = scrape_topics(topic_list)
    # summarize_text(topic_list)

    question_list = {}

    for topic, filename in topic_list.items():
        topic_file = open('./scraped_pages/' + filename + '.txt', 'r', encoding='utf-8') 
        topic_text = topic_file.read()

        print("Keywords:", topic)
        generator = MCQ_Generator(topic_text, keyword_dict[filename])
        print("Distractors:", topic)
        generated_questions = generator.get_MCQs()
        question_list[filename] = generated_questions
        topic_file.close()
        
        print("Results:", topic)
        result = open('./results/' + filename + '.json', 'w', encoding='utf-8')
        result.write(str(generated_questions))


if __name__ == '__main__':
    generate_quiz()
