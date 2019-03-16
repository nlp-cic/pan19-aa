"""
Para usarlo con parametros decomenta lo del main y comenta  la linea que dice  del mainbaseline(),
tambien descomenta la linea 73 y comenta la 74

"""

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed", category=RuntimeWarning)

import time, os, json, glob, codecs
import numpy as np


from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
from sklearn.calibration import CalibratedClassifierCV

#weigth model
from gensim.models.logentropy_model import LogEntropyModel
from gensim.matutils import Scipy2Corpus, corpus2csc
import scipy.sparse as sp

#feature_extraction
from feature_extraction import *

#weka libraries
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection

#cross-validation
from sklearn.model_selection import KFold


#puse los valores fijos
path = "/home/pan19-training-dataset/"
outpath = "/home/pan2019/results/"

#vector que contiene las funciones que obtienen las caracteristicas que se usaran
#lee los valores del archivo feature_extraction
#para agregar funcion tiene que recibir como parametro (*arg)
#se envia (texto, lenguaje), para enviar mas caracteristicas solo agregalas en la funcion get_caracteristicas
#caracteristics = ["func_stop_words", "pos_tag_n_grams", "untyped_character_n_grams", "typed_character_n_grams"]
caracteristics = ["untyped_character_n_grams"]


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


def write_weka_file(features, data, labels, lista, val):
    name = outpath + "output" + str(val) + ".arff"
    with codecs.open(name, 'w', encoding="utf-8") as outputfile:
        outputfile.write("%Title: test\n")
        outputfile.write("@RELATION values\n")

        k = 0
        for value in features:
            outputfile.write("@ATTRIBUTE " + "attr_" + str(k) + " NUMERIC\n")
            k = k+1
        outputfile.write("@ATTRIBUTE class " + str(labels))

        outputfile.write("\n\n@DATA\n")
        for k in range(np.shape(data)[0]):
            for attr in data[k]:
                outputfile.write(str(attr) + ",")
            outputfile.write(str(lista[k]) + "\n")
        outputfile.close()
    return name

def weka_feature_selection(features, train_data, train_labels, problem):
    train_data = train_data.toarray()

    jvm.start(max_heap_size="10g")
    name_file = write_weka_file(features, train_data, set(train_labels), train_labels, re.sub(r"problem", "", problem))
    print("name_file: " + name_file)
    loader = Loader(classname="weka.core.converters.ArffLoader")
    data = loader.load_file(name_file)

    print("X_shape: " + str(np.shape(train_data)))
    attsel = AttributeSelection()
    aseval = ASEvaluation(classname="weka.attributeSelection.CfsSubsetEval")
    assearch = ASSearch(classname="weka.attributeSelection.BestFirst")
    attsel.jwrapper.setEvaluator(aseval.jobject)
    attsel.jwrapper.setSearch(assearch.jobject)
    attsel.select_attributes(data)
    indices = attsel.selected_attributes
    print("selected attribute indices (starting with 0):\n" + str(indices.tolist()))
    valores = indices.tolist()
    print("valores: " + str(valores))
    jvm.stop()

    return valores


def features_selected(X, index_selected):
    selected_features = []
    index_selected_features = 0

    for index in index_selected:
        if index_selected_features == 0:
            selected_features = X[:, [index]]
        else:
            selected_features = np.hstack((selected_features, X[:, [index]]))
        index_selected_features = index_selected_features + 1

    return selected_features

def apply_classification(train_data, train_labels, test_data):
    max_abs_scaler = preprocessing.MaxAbsScaler()
    scaled_train_data = max_abs_scaler.fit_transform(train_data)
    scaled_test_data = max_abs_scaler.transform(test_data)
    clf = CalibratedClassifierCV(OneVsRestClassifier(SVC(C=1)))
    clf.fit(train_data, train_labels)
    predictions = clf.predict(test_data)
    proba = clf.predict_proba(test_data)
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
    """out_data = []
    unk_filelist = glob.glob(path + problem + os.sep + unk_folder + os.sep + '*.txt')
    pathlen = len(path + problem + os.sep + unk_folder + os.sep)
    for i, v in enumerate(predictions):
        out_data.append({'unknown-text': unk_filelist[i][pathlen:], 'predicted-author': v})
    with open(outpath + os.sep + 'answers-' + problem + '.json', 'w') as f:
        json.dump(out_data, f, indent=4)"""

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

        # Building test set
        train_texts = [text for i, (text, label) in enumerate(train_docs)]
        train_labels = [label for i, (text, label) in enumerate(train_docs)]
        labels = np.array([int(re.sub(r"candidate", "", k)) for k in train_labels])

        docs = extract_vocabulary(train_docs)
        vectorizer = CountVectorizer(lowercase=False, tokenizer=lambda x: x.split('&%$'))

        train_data = vectorizer.fit_transform(docs)
        features = vectorizer.get_feature_names()

        ############################################################################
        ## cross-validation ##
        """print(np.shape(train_data))
        kf = KFold(n_splits=5, shuffle=True)
        for train_index, test_index in kf.split(train_data):
            #print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = train_data[train_index], train_data[test_index]
            #y_train, y_test = labels[train_index], labels[test_index]
            y_train = [train_labels[k] for k in train_index]
            y_test = [train_labels[k] for k in test_index]
            #print("------------------------------")
            #print(np.shape(X_train))
            #print(np.shape(X_test))
            
            ndoc, nterm = X_train.shape
            Xc = Scipy2Corpus(X_train)
            log_ent = LogEntropyModel(Xc)
            X_train = log_ent[Xc]
            X_train = corpus2csc(X_train, num_terms=nterm, num_docs=ndoc)
            X_train = sp.csc_matrix.transpose(X_train)

            indices = weka_feature_selection(features, X_train, y_train, problem)
            X_train = features_selected(X_train, indices)

            ndoc, nterm = X_test.shape
            Xc = Scipy2Corpus(X_test)
            log_ent = LogEntropyModel(Xc)
            X_test = log_ent[Xc]
            X_test = corpus2csc(X_test, num_terms=nterm, num_docs=ndoc)
            X_test = sp.csc_matrix.transpose(X_test)
            X_test = features_selected(X_test, indices)
            print(np.shape(X_train))
            print(np.shape(X_test))


        exit()"""

        #weight LogEntropy
        ndoc, nterm = train_data.shape
        Xc = Scipy2Corpus(train_data)
        log_ent = LogEntropyModel(Xc)
        train_data = log_ent[Xc]
        train_data = corpus2csc(train_data, num_terms=nterm, num_docs=ndoc)
        train_data = sp.csc_matrix.transpose(train_data)

        ############################################################################
        ## weka ##
        #train_data = train_data.toarray()

        ############################################################################


        # Building test set
        test_docs = read_files(path + os.sep + problem, unk_folder)
        test_texts = [text for i, (text, label) in enumerate(test_docs)]
        docs_test = extract_vocabulary(test_docs)
        test_data = vectorizer.transform(docs_test)

        print('\t', 'language: ', language[index])
        print('\t', len(candidates), 'candidate authors')
        print('\t', len(train_texts), 'known texts')
        print('\t', len(test_texts), 'unknown texts')


        #weight LogEntropy
        ndoc, nterm = test_data.shape
        Xc = Scipy2Corpus(test_data)
        log_ent = LogEntropyModel(Xc)
        test_data = log_ent[Xc]
        test_data = corpus2csc(test_data, num_terms=nterm, num_docs=ndoc)
        test_data = sp.csc_matrix.transpose(test_data)



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