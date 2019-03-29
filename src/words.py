# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('TreeTagger')
logger.propagate = False
import nltk
from nltk import tokenize
from string import punctuation
import re

import treetaggerwrapper as ttw
from cic.stop_words import english, french, italian, spanish


#--------------------------------------------------------------------------------------------------------------------
#preprocessing
def clean_text(text):
    return re.sub(r" +", " ", re.sub(r"\t", " ", re.sub(r"(\n|\r)+", "\n", text)))

def pre_proc_text(text):
    return re.sub("\\d+", "0", clean_text(text)).lower()


#--------------------------------------------------------------------------------------------------------------------
def bag_of_words(text, current_language):
    tokens = tokenize.word_tokenize(text=text, language=current_language)

    return tokens

#--------------------------------------------------------------------------------------------------------------------
def pos_tag_n_grams(text, size_grams, current_language):
    text = re.sub(r" +", " ", re.sub(r"\.", "\. ", pre_proc_text(text)))
    #n = [1, 4]#range(1, 6)

    tagger = ttw.TreeTagger(TAGLANG=(current_language[0:2] if current_language[0:2] != "sp" else "es"))
    values = tagger.tag_text(text)

    tags2 = ttw.make_tags(values)

    tags = []
    for tag in tags2:
        if isinstance(tag, ttw.NotTag):
            tags.append("unk")
        else:
            tags.append(tag[1])

    return "|~|".join(tags)

#--------------------------------------------------------------------------------------------------------------------
def func_stop_words(text, size_grams, current_language):
    #sizes = [5]#range(1, 9)

    if current_language == 'en':
        current_language = 'english'
        stop_words = english
    elif current_language == 'fr':
        current_language = 'french'
        stop_words = french
    elif current_language == 'it':
        current_language = 'italian'
        stop_words = italian
    elif current_language == 'sp':
        current_language = 'spanish'
        stop_words = spanish
    else:
        print('FATAL language not found')
    
    text = re.sub(r" +", " ", re.sub(r"\n", " ", pre_proc_text(text)))
    values = tokenize.word_tokenize(text=text, language=current_language)
    tokens = []

    for i in range(len(values)):
        if values[i] in stop_words:
            tokens.append(stop_words[stop_words.index(values[i])])

    return "|~|".join(tokens)


# -------------------------------------------------------------------------------------
# affix
def func_prefix(text, size_grams, current_language):
    tokens = []
    text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text))).split(" ")
    for i in range(len(text)):
        if len(text[i]) > size_grams:
            tokens.append(text[i][:size_grams])

    return "|~|".join(tokens)


def func_sufix(text, size_grams, current_language):
    tokens = []
    text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text))).split(" ")
    for i in range(len(text)):
        if len(text[i]) > size_grams:
            tokens.append(text[i][-size_grams:])

    return "|~|".join(tokens)


def func_space_prefix(text, size_grams, current_language):
    global punctuation
    tokens = []
    paragraphs = pre_proc_text(text).split("\n")
    for paraph in paragraphs:
        values = paraph.split(" ")[1:]
        for token in values:
            if len(token) > size_grams - 2 and re.search("[" + punctuation + "]", token[:(size_grams - 1)]) is None:
                tokens.append("_" + token[:(size_grams - 1)])

    return "|~|".join(tokens)


def func_space_sufix(text, size_grams, current_language):
    global punctuation
    tokens = []
    paragraphs = pre_proc_text(text).split("\n")
    for paraph in paragraphs:
        values = paraph.split(" ")[:-1]
        for token in values:
            if len(token) > size_grams - 2 and re.search("[" + punctuation + "]", token[-(size_grams - 1):]) is None:
                tokens.append(token[-(size_grams - 1):])
    return "|~|".join(tokens)


# -------------------------------------------------------------------------------------
# word
def func_whole_word(text, size_grams):
    tokens = []
    text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text))).split(" ")

    for word in text:
        if len(word) == size_grams:
            tokens.append(word)

    return " ".join(tokens)


def func_mid_word(text, size_grams):
    tokens = []
    text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text))).split(" ")
    for word in text:
        if len(word) >= size_grams + 2:
            for j in range(1, len(word) - size_grams, 1):
                tokens.append(word[j: j + size_grams])

    return " ".join(tokens)


def func_multi_word(text, size_grams):
    global punctuation
    tokens = []
    if size_grams < 3:
        return tokens

    words = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text))).split(" ")
    for i in range(len(words) - 1):
        if re.search("(.*)[" + punctuation + "]+$", words[i]) is None and re.search("^[" + punctuation + "]+(.*)",
                                                                                    words[i + 1]) is None:
            j = len(words[i]) - (size_grams - 2) if len(words[i]) - (size_grams - 2) >= 0 else 0
            m = 1 + ((len(words[i]) - (size_grams - 2)) * -1 if len(words[i]) - (size_grams - 2) < 0 else 0)
            while True:
                if j >= len(words[i]) or m > len(words[i + 1]):
                    break

                if re.search("[" + punctuation + "]", words[i][j: len(words[i])]) is None and \
                        re.search("[" + punctuation + "]", words[i + 1][: m]) is None:
                    word = words[i][j: len(words[i])] + "_" + words[i + 1][: m]
                    tokens.append(word)
                j += 1
                m += 1

    return " ".join(tokens)


# -------------------------------------------------------------------------------------
# punct
def func_beg_punct(text, size_grams, current_language):
    global punctuation
    tokens = []
    paragraphs = pre_proc_text(text).split("\n")
    for paraph in paragraphs:
        for k in range(len(paraph) - (size_grams - 1)):
            if paraph[k] in punctuation and re.search("[" + punctuation + "]", paraph[k + 1: k + size_grams]) is None:
                tokens.append(paraph[k: k + size_grams])

    return "|~|".join(tokens)


def func_mid_punct(text, size_grams, current_language):
    global punctuation
    tokens = []

    if size_grams == 3:
        for token in text.split():
            if token in punctuation:
                tokens.append(token)
    else:
        if size_grams < 3:
            return tokens
        values = re.sub(r"\n", " ", text).split(" ")

        for i in range(len(values)):
            if re.search("^[" + punctuation + "]*([^" + punctuation + "])+[" + punctuation + "]+(([^" + punctuation
                         + "])+[" + punctuation + "]*)$", values[i]) is not None:
                val = False
                m = -1
                for k in range(len(punctuation)):
                    m = values[i].find(punctuation[k])
                    if m > 0 and m < len(values[i]) - 1:
                        val = True
                        break
                if val:
                    k = m if size_grams - 2 > m else size_grams - 2
                    w = size_grams - m if size_grams - 2 > m else 2
                    while True:
                        word = values[i][(m - k): (m + w)]
                        w += 1
                        k -= 1
                        tokens.append(word)
                        if k <= 0 or len(values[i][(m - k): (m + w)]) != size_grams:
                            break

    return "|~|".join(tokens)


def func_end_punct(text, size_grams, current_language):
    global punctuation
    tokens = []
    paragraphs = pre_proc_text(text).split("\n")
    for paraph in paragraphs:
        for k in range(len(paraph) - (size_grams - 1)):
            if paraph[k + (size_grams - 1)] in punctuation and re.search("[" + punctuation + "]",
                                                                         paraph[k: k + (size_grams - 1)]) is None:
                tokens.append(paraph[k: k + size_grams])

    return "|~|".join(tokens)
'''
#tokenizer = RegexpTokenizer('\s+', gaps=True)
print('test')
tokenizer = tokenize.RegexpTokenizer(r'[|~|]+', gaps=True)
s = "Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\n\nThanks."
t = func_stop_words(s, 3, 'en')
print(t)
print(tokenizer.tokenize(t))'''