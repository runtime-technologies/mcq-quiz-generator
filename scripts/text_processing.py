from summarizer import Summarizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
import pke
import string


def summarize_text(topic_list):
    for topic, filename in topic_list.items():
        topic_file = open('./scraped_page/' + filename +
                          '_summarised.txt', 'w', encoding='utf-8')
        text = topic_file.read()
        model = Summarizer()
        result = model(text, min_length=60, max_length=500, ratio=0.4)
        summarized_text = ''.join(result)
        topic_file.write(summarized_text)
        topic_file.close()


def get_nouns_multipartite(text):
    keywords = []

    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input=text)

    # Ignore punctuations and stopwords
    pos = {'PROPN'}
    #pos = {'VERB', 'ADJ', 'NOUN'}

    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')

    # Build the Multipartite graph and rank candidates using random walk,
    # alpha controls the weight adjustment mechanism, see TopicRank for
    # threshold/method parameters.
    extractor.candidate_selection(pos=pos, stoplist=stoplist)
    extractor.candidate_weighting(alpha=1.1, threshold=0.75, method='average')

    keyphrases = extractor.get_n_best(n=20)

    for key in keyphrases:
        keywords.append(key[0])

    return keywords


def generate_keywords(text, summarised_text):
    keywords = get_nouns_multipartite(text)

    filtered_keys = []
    for keyword in keywords:
        if keyword.lower() in summarised_text.lower():
            filtered_keys.append(keyword)

    print(filtered_keys)
