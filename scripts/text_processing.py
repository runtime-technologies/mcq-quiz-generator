from summarizer import Summarizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
import pke
import string


def summarize_text(topic_list):
    model = Summarizer()
    for filename in topic_list.values():
        topic_file = open('./scraped_pages/' + filename +
                          '.txt', 'r', encoding='utf-8')
        summary_file = open('./scraped_pages/' + filename +
                            '_summarised.txt', 'w', encoding='utf-8')
        text = topic_file.read()
        result = model(text, min_length=60, max_length=500, ratio=0.4)
        summarized_text = ''.join(result)
        summary_file.write(summarized_text)
        topic_file.close()
        summary_file.close()


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
    filtered_keys = keywords
    # filtered_keys = []
    # for word in keywords:
    #     if word.lower() in summarised_text.lower():
    #         filtered_keys.append(word)

    return filtered_keys


def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    # Remove any short sentences less than 20 letters.
    sentences = [sentence.strip()
                 for sentence in sentences if len(sentence) > 20]
    return sentences


def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)

    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
    return keyword_sentences


def get_mapped_sentences(text):
    filtered_keys = generate_keywords(text, "")
    # filtered_keys = keywords
    sentences = tokenize_sentences(text)
    keyword_sentence_mapping = get_sentences_for_keyword(filtered_keys, sentences)

    return keyword_sentence_mapping
