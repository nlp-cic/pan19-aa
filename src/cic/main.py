"""
Para usarlo con parametros decomenta lo del main y comenta  la linea que dice  del mainbaseline(),
tambien descomenta la linea 73 y comenta la 74

"""

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed", category=RuntimeWarning)

import time, os, json, glob, codecs
import numpy as np
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from nltk import tokenize
import argparse

from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
from sklearn.calibration import CalibratedClassifierCV
from feature_extraction import *

#puse los valores fijos
path = "/home/pan19-training-dataset/"
outpath = "/home/pan2019/results/"

#vector que contiene las funciones que obtienen las caracteristicas que se usaran
#lee los valores del archivo feature_extraction
#para agregar funcion tiene que recibir como parametro (*arg)
#se envia (texto, lenguaje), para enviar mas caracteristicas solo agregalas en la funcion get_caracteristicas
caracteristics = ["func_stop_words", "pos_tag_n_grams", "untyped_character_n_grams", "typed_character_n_grams"]


def get_caracteristics(text):
    tokens = []
    for val in caracteristics:
        tokens.extend(globals()[val](text, current_language))

    return tokens

def extract_vocabulary(texts):
    docs = []
    for (text, label) in texts:
        text_occurrences = get_caracteristics(text)
        docs.append('&%$'.join(text_occurrences))

    return docs

def read_files(path, label):
    # Reads all text files located in the 'path' and assigns them to 'label' class
    files = glob.glob(path + os.sep + label + os.sep + '*.txt')
    texts = []
    for i, v in enumerate(files):
        f = codecs.open(v, 'r', encoding='utf-8')
        texts.append((f.read(), label))
        f.close()

    return texts

def valid_language(language):
    global current_language

    if language == 'en':
        current_language = 'english'
    elif language == 'fr':
        current_language = 'french'
    elif language == 'it':
        current_language = 'italian'
    elif language == 'sp':
        current_language = 'spanish'

#def baseline(path, outpath, n=3, ft=5, pt=0.1):
def baseline():
    start_time = time.time()
    infocollection = path + 'collection-info.json'
    problems = []
    language = []
    with open(infocollection, 'r') as f:
        for attrib in json.load(f):
            problems.append(attrib['problem-name'])
            language.append(attrib['language'])
    for index, problem in enumerate(problems):
        print(problem)
        valid_language(language[index])
        # Reading information about the problem
        infoproblem = path + problem + os.sep + 'problem-info.json'
        candidates = []
        with open(infoproblem, 'r') as f:
            fj = json.load(f)
            unk_folder = fj['unknown-folder']
            for attrib in fj['candidate-authors']:
                candidates.append(attrib['author-name'])
                # Building training set
        train_docs = []
        for candidate in candidates:
            train_docs.extend(read_files(path + os.sep + problem, candidate))

        train_texts = [text for i, (text, label) in enumerate(train_docs)]
        train_labels = [label for i, (text, label) in enumerate(train_docs)]

        #como no tenemos propiamente un diccionario por los tipos de características que estamos usando
        #CountVectorizer se utiliza de esta forma, en el metodo extract_vocabulary se especifica el símbolo
        #con el que se separan las características (&%$)
        docs = extract_vocabulary(train_docs)
        vectorizer = CountVectorizer(lowercase=False, min_df=2, tokenizer=lambda x: x.split('&%$'))

        train_data = vectorizer.fit_transform(docs)
        train_data = train_data.astype(float)
        for i, v in enumerate(train_texts):
            train_data[i] = train_data[i] / len(train_texts[i])
        print('\t', 'language: ', language[index])
        print('\t', len(candidates), 'candidate authors')
        print('\t', len(train_texts), 'known texts')
        # Building test set
        test_docs = read_files(path + os.sep + problem, unk_folder)
        test_texts = [text for i, (text, label) in enumerate(test_docs)]
        test_data = vectorizer.transform(test_texts)
        test_data = test_data.astype(float)
        for i, v in enumerate(test_texts):
            test_data[i] = test_data[i] / len(test_texts[i])
        print('\t', len(test_texts), 'unknown texts')
        # Applying SVM
        max_abs_scaler = preprocessing.MaxAbsScaler()
        scaled_train_data = max_abs_scaler.fit_transform(train_data)
        scaled_test_data = max_abs_scaler.transform(test_data)
        clf = CalibratedClassifierCV(OneVsRestClassifier(SVC(C=1)))
        clf.fit(scaled_train_data, train_labels)
        predictions = clf.predict(scaled_test_data)
        proba = clf.predict_proba(scaled_test_data)
        # Reject option (used in open-set cases)
        pt = 0.1
        count = 0
        for i, p in enumerate(predictions):
            sproba = sorted(proba[i], reverse=True)
            if sproba[0] - sproba[1] < pt:
                predictions[i] = u'<UNK>'
                count = count + 1
        print('\t', count, 'texts left unattributed')
        # Saving output data
        out_data = []
        unk_filelist = glob.glob(path + problem + os.sep + unk_folder + os.sep + '*.txt')
        pathlen = len(path + problem + os.sep + unk_folder + os.sep)
        for i, v in enumerate(predictions):
            out_data.append({'unknown-text': unk_filelist[i][pathlen:], 'predicted-author': v})
        with open(outpath + os.sep + 'answers-' + problem + '.json', 'w') as f:
            json.dump(out_data, f, indent=4)


        #neigh = KNeighborsClassifier(n_neighbors=3)
        #neigh.fit(X, y)

        print('elapsed time:', time.time() - start_time)


def main():
    """parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='PAN-19 Baseline Authorship Attribution Method')
    parser.add_argument('-i', type=str, help='Path to the main folder of a collection of attribution problems')
    parser.add_argument('-o', type=str, help='Path to an output folder')
    parser.add_argument('-n', type=int, default=3, help='n-gram order (default=3)')
    parser.add_argument('-ft', type=int, default=5, help='frequency threshold (default=5)')
    parser.add_argument('-pt', type=float, default=0.1, help='probability threshold for the reject option (default=0.1')
    args = parser.parse_args()
    if not args.i:
        print('ERROR: The input folder is required')
        parser.exit(1)
    if not args.o:
        print('ERROR: The output folder is required')
        parser.exit(1)

    baseline(args.i, args.o, args.n, args.ft, args.pt)"""
    baseline()


if __name__ == '__main__':
    main()