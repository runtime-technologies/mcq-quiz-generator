from scripts.text_processing import get_mapped_sentences

import requests
import re
import random
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk, cosine_lesk, simple_lesk
from nltk.corpus import wordnet as wn


class MCQ_Generator:
    def __init__(self, text, summary):
        self.text = text
        self.summary = summary

    def get_wordsense(self, sent, word):
        word = word.lower()

        if len(word.split()) > 0:
            word = word.replace(" ", "_")

        synsets = wn.synsets(word, 'n')
        if synsets:
            wup = max_similarity(sent, word, 'wup', pos='n')
            adapted_lesk_output = adapted_lesk(sent, word, pos='n')
            lowest_index = min(synsets.index(
                wup), synsets.index(adapted_lesk_output))
            return synsets[lowest_index]
        else:
            return None

    def get_distractors_wordnet(self, syn, word):
        distractors = []
        word = word.lower()
        orig_word = word
        if len(word.split()) > 0:
            word = word.replace(" ", "_")
        hypernym = syn.hypernyms()
        if len(hypernym) == 0:
            return distractors
        for item in hypernym[0].hyponyms():
            name = item.lemmas()[0].name()
            if name == orig_word:
                continue
            name = name.replace("_", " ")
            name = " ".join(w.capitalize() for w in name.split())
            if name is not None and name not in distractors:
                distractors.append(name)
        return distractors

    def get_distractors_conceptnet(self, word):
        word = word.lower()
        original_word = word
        if (len(word.split()) > 0):
            word = word.replace(" ", "_")
        distractor_list = []
        url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5" % (
            word, word)
        obj = requests.get(url).json()

        for edge in obj['edges']:
            link = edge['end']['term']

            url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10" % (
                link, link)
            obj2 = requests.get(url2).json()
            for edge in obj2['edges']:
                word2 = edge['start']['label']
                if word2 not in distractor_list and original_word.lower() not in word2.lower():
                    distractor_list.append(word2)

        return distractor_list

    def get_distractors(self, keyword_sentence_mapping):
        key_distractor_list = {}

        for keyword in keyword_sentence_mapping:
            wordsense = self.get_wordsense(
                keyword_sentence_mapping[keyword][0], keyword)

            if wordsense:
                distractors = self.get_distractors_wordnet(wordsense, keyword)
                if len(distractors) == 0:
                    distractors = self.get_distractors_conceptnet(keyword)
                if len(distractors) != 0:
                    key_distractor_list[keyword] = distractors
            else:

                distractors = self.get_distractors_conceptnet(keyword)
                if len(distractors) != 0:
                    key_distractor_list[keyword] = distractors

        return key_distractor_list

    def get_MCQs(self):
        keyword_sentence_mapping = get_mapped_sentences(
            self.text, self.summary)
        key_distractor_list = self.get_distractors(keyword_sentence_mapping)

        question_list = []

        for each in key_distractor_list:
            mcq = {}
            question = keyword_sentence_mapping[each][0]
            pattern = re.compile(each, re.IGNORECASE)
            question = pattern.sub(" _______ ", question)
            mcq['question'] = question
            mcq['answer'] = each

            choices = [each.capitalize()] + key_distractor_list[each]
            options = choices[:4]
            random.shuffle(options)
            mcq['options'] = options

            question_list.append(mcq)

        return question_list
