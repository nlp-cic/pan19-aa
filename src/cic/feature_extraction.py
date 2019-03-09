from nltk import tokenize
from collections import defaultdict
import re
from string import punctuation

import treetaggerwrapper as ttw
import pprint
from stop_words import english, french, italian, spanish



#--------------------------------------------------------------------------------------------------------------------
#preprocessing
def clean_text(text):
	return re.sub(r" +", " ", re.sub(r"\t", " ", re.sub(r"(\n|\r)+", "\n", text)))

def pre_proc_text(text):
	return re.sub("\\d+", "0", clean_text(text)).lower()


#--------------------------------------------------------------------------------------------------------------------
def bag_of_words(text, lang):
	tokens = tokenize.word_tokenize(text=text, language=lang)

	return tokens

#--------------------------------------------------------------------------------------------------------------------
def pos_tag_n_grams(*arg):
	current_language = arg[1]
	text = re.sub(r" +", " ", re.sub(r"\.", "\. ", pre_proc_text(arg[0])))
	n = [1]#range(1, 6)

	#tagger = TreeTagger(language=current_language)
	tagger = ttw.TreeTagger(TAGLANG=(current_language[0:2] if current_language[0:2] != "sp" else "es"))
	values = tagger.tag_text(text)

	tags2 = ttw.make_tags(values)

	tags = []
	for tag in tags2:
		if isinstance(tag, ttw.NotTag):
			tags.append("unk")
		else:
			tags.append(tag[1])

	tokens = []
	for values in n:
		j = 0
		while j < len(tags) - (values - 1):
			tokens.append('_'.join(tags[j: j + values]) + "_pos_" + str(values))
			j = j + 1

	return tokens

#--------------------------------------------------------------------------------------------------------------------
def func_stop_words(*arg):
	current_language = arg[1]
	n_grams = []

	sizes = [8]#range(1, 9)

	if current_language == 'english':
		stop_words = english
	if current_language == 'french':
		stop_words = french
	if current_language == 'italian':
		stop_words = italian
	if current_language == 'spanish':
		stop_words = spanish

	text = re.sub(r" +", " ", re.sub(r"\n", " ", pre_proc_text(arg[0])))
	values = tokenize.word_tokenize(text=text, language=current_language)
	tokens = []

	for i in range(len(values)):
		if values[i] in stop_words:
			tokens.append(stop_words[stop_words.index(values[i])])

	for k in sizes:
		n_grams.extend([('_'.join(tokens[i:i + k])) + "_nsw_" + str(k) for i in range(len(tokens) - k + 1)])

	return n_grams


def untyped_character_n_grams(*args):
	sizes = [3] #range(3, 5)
	untyped = []
	text = pre_proc_text(args[0])

	for size in sizes:
		for paragraph in text.split('\n'):
			for i in range(0, len(paragraph) - (size - 1)):
				untyped.append(paragraph[i:i + size] + "_np_" + str(size))

	return untyped

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
def typed_character_n_grams(text, sizes):
	tokens = []

	for size_grams in sizes:
		tokens.extend(func_prefix(size_grams, text))
		tokens.extend(func_sufix(size_grams, text))
		tokens.extend(func_space_prefix(size_grams, text))
		tokens.extend(func_space_sufix(size_grams, text))
		tokens.extend(func_whole_word(size_grams, text))
		tokens.extend(func_mid_word(size_grams, text))
		tokens.extend(func_multi_word(size_grams, text))
		tokens.extend(func_beg_punct(size_grams, text))
		tokens.extend(func_mid_punct(size_grams, text))
		tokens.extend(func_end_punct(size_grams, text))

	return tokens


# -------------------------------------------------------------------------------------
# affix
def func_prefix(size_grams, text):
	tokens = []
	text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text, True))).split(" ")
	for i in range(len(text)):
		if len(text[i]) > size_grams:
			tokens.append(text[i][:size_grams] + "_pf_" + str(size_grams))

	return tokens


def func_sufix(size_grams, text):
	tokens = []
	text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text, True))).split(" ")
	for i in range(len(text)):
		if len(text[i]) > size_grams:
			tokens.append(text[i][-size_grams:] + "_sf_" + str(size_grams))

	return tokens


def func_space_prefix(size_grams, text):
	global punctuation
	tokens = []
	paragraphs = pre_proc_text(text).split("\n")
	for paraph in paragraphs:
		values = paraph.split(" ")[1:]
		for token in values:
			if len(token) > size_grams - 2 and re.search("[" + punctuation + "]", token[:(size_grams - 1)]) is None:
				tokens.append("_" + token[:(size_grams - 1)] + "_sp_" + str(size_grams))

	return tokens


def func_space_sufix(size_grams, text):
	global punctuation
	tokens = []
	paragraphs = pre_proc_text(text).split("\n")
	for paraph in paragraphs:
		values = paraph.split(" ")[:-1]
		for token in values:
			if len(token) > size_grams - 2 and re.search("[" + punctuation + "]", token[-(size_grams - 1):]) is None:
				tokens.append(token[-(size_grams - 1):] + "_" + "_ss_" + str(size_grams))
	return tokens


# -------------------------------------------------------------------------------------
# word
def func_whole_word(size_grams, text):
	tokens = []
	text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text, True))).split(" ")

	for word in text:
		if len(word) == size_grams:
			tokens.append(word + "_ww_" + str(size_grams))

	return tokens


def func_mid_word(size_grams, text):
	tokens = []
	text = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text, True))).split(" ")
	for word in text:
		if len(word) >= size_grams + 2:
			for j in range(1, len(word) - size_grams, 1):
				tokens.append(word[j: j + size_grams] + "_mw_" + str(size_grams))

	return tokens


def func_multi_word(size_grams, text):
	global punctuation
	tokens = []
	if size_grams < 3:
		return tokens

	words = re.sub(r"\s+", " ", re.sub(r"\n", " ", pre_proc_text(text, True))).split(" ")
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
					tokens.append(word + "_lw_" + str(size_grams))
				j += 1
				m += 1

	return tokens


# -------------------------------------------------------------------------------------
# punct
def func_beg_punct(size_grams, text):
	global punctuation
	tokens = []
	paragraphs = pre_proc_text(text).split("\n")
	for paraph in paragraphs:
		for k in range(len(paraph) - (size_grams - 1)):
			if paraph[k] in punctuation and re.search("[" + punctuation + "]", paraph[k + 1: k + size_grams]) is None:
				tokens.append(paraph[k: k + size_grams] + "_bp_" + str(size_grams))

	return tokens


def func_mid_punct(size_grams, text):
	global punctuation
	tokens = []

	if size_grams == 3:
		for token in text.split():
			if token in punctuation:
				tokens.append(token + "mp_" + str(size_grams))
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
						tokens.append(word + "_mp_" + str(size_grams))
						if k <= 0 or len(values[i][(m - k): (m + w)]) != size_grams:
							break

	return tokens


def func_end_punct(size_grams, text):
	global punctuation
	tokens = []
	paragraphs = pre_proc_text(text).split("\n")
	for paraph in paragraphs:
		for k in range(len(paraph) - (size_grams - 1)):
			if paraph[k + (size_grams - 1)] in punctuation and re.search("[" + punctuation + "]",
																		 paraph[k: k + (size_grams - 1)]) is None:
				tokens.append(paraph[k: k + size_grams] + "_ep_" + str(size_grams))

	return tokens