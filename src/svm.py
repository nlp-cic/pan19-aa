# -*- coding: utf-8 -*-

"""
 A baseline authorship attribution method 
 based on a character n-gram representation
 and a linear SVM classifier.
 It has a reject option to leave documents unattributed
 (when the probabilities of the two most likely training classes are too close)
 
 Questions/comments: stamatatos@aegean.gr

 It can be applied to datasets of PAN-19 cross-domain authorship attribution task
 See details here: http://pan.webis.de/clef19/pan19-web/author-identification.html
 Dependencies:
 - Python 2.7 or 3.6 (we recommend the Anaconda Python distribution)
 - scikit-learn

 Usage from command line: 
    > python pan19-cdaa-baseline.py -i EVALUATION-DIRECTORY -o OUTPUT-DIRECTORY [-n N-GRAM-ORDER] [-ft FREQUENCY-THRESHOLD] [-pt PROBABILITY-THRESHOLD]
 EVALUATION-DIRECTORY (str) is the main folder of a PAN-19 collection of attribution problems
 OUTPUT-DIRECTORY (str) is an existing folder where the predictions are saved in the PAN-19 format
 Optional parameters of the model:
   N-GRAM-ORDER (int) is the length of character n-grams (default=3)
   FREQUENCY-THRESHOLD (int) is the cutoff threshold used to filter out rare n-grams (default=5)
   PROBABILITY-THRESHOLD (float) is the threshold for the reject option assigning test documents to the <UNK> class (default=0.1)
                                 Let P1 and P2 be the two maximum probabilities of training classes for a test document. If P1-P2<pt then the test document is assigned to the <UNK> class.
   
 Example:
     > python pan19-cdaa-baseline.py -i "pan19_CDAA_trainingDataset" -o "results/svm"
"""

from __future__ import print_function
import os
import glob
import json
import argparse
import time
import codecs
import pathlib2
import pandas as pd
from collections import defaultdict
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
from sklearn.calibration import CalibratedClassifierCV
from numpy import arange
from nltk.tokenize import RegexpTokenizer
from evaluator import evaluate_all
from util import empty_call, empty_call2, regular, reg_low, update_results
from struct_ import length_words, range_words_2, range_words_3, range_words_4, range_words_5, \
length_sent_by_words, range_sent_by_words_3, range_sent_by_chars_5
from punct import punct_, whitesp, acc, vow, cons, up, acc_vow_up
from vowel import vowels, vowels_with_stars, vowels_with_withesp
from words import pos_tag_n_grams, func_stop_words, func_prefix, func_sufix, func_space_prefix, \
func_space_sufix, func_beg_punct, func_mid_punct, func_end_punct

word_methods = ['stop_words', 'prefix', 'sufix', 'space_prefix', 'space_sufix', 'beg_punct', 'mid_punct', 'end_punct'] #, 'pos_tag'

def represent_text3(text, type_ngram, size_grams, language):
    switcher = {
        'pos_tag': pos_tag_n_grams,
        'stop_words': func_stop_words,
        'prefix': func_prefix,
        'sufix': func_sufix,
        'space_prefix': func_space_prefix,
        'space_sufix': func_space_sufix,
        'beg_punct': func_beg_punct,
        'mid_punct': func_mid_punct,
        'end_punct': func_end_punct
    }
    func = switcher.get(type_ngram, empty_call2)
    return func(text, size_grams, language)

def represent_text2(text, type_ngram):
    switcher = {
        'regular': regular,
        'reg_low': reg_low,
        'struct_len_word': length_words,
        'struct_len_sent': length_sent_by_words,
        'struct_range_word_2': range_words_2,
        'struct_range_word_3': range_words_3,
        'struct_range_word_4': range_words_4,
        'struct_range_word_5': range_words_5,
        'struct_range_sent_word_3': range_sent_by_words_3,
        'struct_range_sent_char_5': range_sent_by_chars_5,
        'punct_punct': punct_,
        'punct_whitesp': whitesp,
        'punct_acc': acc,
        'punct_vow': vow,
        'punct_cons': cons,
        'punct_up': up,
        'punct_acc_vow_up': acc_vow_up,
        'vow': vowels,
        'vow_star': vowels_with_stars,
        'vow_whit': vowels_with_withesp
    }
    func = switcher.get(type_ngram, empty_call)
    return func(text)
    
def represent_text(text,n,type_ngram):
    text = represent_text2(text, type_ngram)
    
    # Extracts all character 'n'-grams from  a 'text'
    if n>0:
        tokens = [text[i:i+n] for i in range(len(text)-n+1)]
    frequency = defaultdict(int)
    for token in tokens:
        frequency[token] += 1
    return frequency

def read_files(path,label):
    # Reads all text files located in the 'path' and assigns them to 'label' class
    files = glob.glob(path+os.sep+label+os.sep+'*.txt')
    texts=[]
    for i,v in enumerate(files):
        f=codecs.open(v,'r',encoding='utf-8')
        texts.append((f.read(),label))
        f.close()
    return texts

def extract_vocabulary(texts,n,ft,type_ngram):
    # Extracts all characer 'n'-grams occurring at least 'ft' times in a set of 'texts'
    occurrences=defaultdict(int)
    for (text, label) in texts:
        text_occurrences=represent_text(text,n,type_ngram)
        for ngram in text_occurrences:
            if ngram in occurrences:
                occurrences[ngram]+=text_occurrences[ngram]
            else:
                occurrences[ngram]=text_occurrences[ngram]
    vocabulary=[]
    for i in occurrences.keys():
        if occurrences[i]>=ft:
            vocabulary.append(i)
    return vocabulary

def baseline(path, outpath, n=3, ft=5, pt=0.1, type_ngram='regular'):
    start_time = time.time()
    # Reading information about the collection
    infocollection = path+os.sep+'collection-info.json'
    problems = []
    language = []
    with open(infocollection, 'r') as f:
        for attrib in json.load(f):
            problems.append(attrib['problem-name'])
            language.append(attrib['language'])
    for index,problem in enumerate(problems):
        print(problem)
        # Reading information about the problem
        infoproblem = path+os.sep+problem+os.sep+'problem-info.json'
        candidates = []
        with open(infoproblem, 'r') as f:
            fj = json.load(f)
            unk_folder = fj['unknown-folder']
            for attrib in fj['candidate-authors']:
                candidates.append(attrib['author-name'])
        # Building training set
        train_docs=[]
        for candidate in candidates:
            train_docs.extend(read_files(path+os.sep+problem,candidate))
        train_texts = [text for i,(text,label) in enumerate(train_docs)]
        train_labels = [label for i,(text,label) in enumerate(train_docs)]
        
        if type_ngram in word_methods:
            modified_train_texts = [represent_text3(txt, type_ngram, 3, language[index]) for txt in train_texts]
            tokenizer_ = RegexpTokenizer(r'[|~|]+', gaps=True)
            vectorizer = CountVectorizer(analyzer='word', ngram_range=(n,n), lowercase=False, \
                                                                                        tokenizer=tokenizer_.tokenize, min_df=5)
        else:
            modified_train_texts = [represent_text2(txt, type_ngram) for txt in train_texts]
            vocabulary = extract_vocabulary(train_docs, n, ft, type_ngram)
            vectorizer = CountVectorizer(analyzer='char', ngram_range=(n,n), lowercase=False, vocabulary=vocabulary)
        try:
            train_data = vectorizer.fit_transform(modified_train_texts)
        except ValueError:
            print('Empty vocabulary, setting frequency threshold as 1')
            if type_ngram in word_methods:
                vectorizer = CountVectorizer(analyzer='word', ngram_range=(n,n), lowercase=False, \
                                                                                        tokenizer=tokenizer_.tokenize, min_df=1)
            else:
                vocabulary = extract_vocabulary(train_docs, n, 1, type_ngram)
                vectorizer = CountVectorizer(analyzer='char', ngram_range=(n,n), lowercase=False, vocabulary=vocabulary)
            train_data = vectorizer.fit_transform(modified_train_texts)
            
        train_data = train_data.astype(float)
        for i,v in enumerate(train_texts):
            train_data[i]=train_data[i]/len(train_texts[i])
        print('\t', 'language: ', language[index])
        print('\t', len(candidates), 'candidate authors')
        print('\t', len(train_texts), 'known texts')
        if type_ngram not in word_methods:
            print('\t', 'vocabulary size:', len(vocabulary))
        else:
            print('\t', 'train_data size', train_data.shape)
        # Building test set
        test_docs=read_files(path+os.sep+problem,unk_folder)
        test_texts = [text for i,(text,label) in enumerate(test_docs)]
        if type_ngram in word_methods:
            modified_test_texts = [represent_text3(txt, type_ngram, 3, language[index]) for txt in test_texts]
        else:
            modified_test_texts = [represent_text2(txt, type_ngram) for txt in test_texts]
        test_data = vectorizer.transform(modified_test_texts)
        #test_data = vectorizer.transform(test_texts)
        test_data = test_data.astype(float)
        for i,v in enumerate(test_texts):
            test_data[i]=test_data[i]/len(test_texts[i])
        print('\t', len(test_texts), 'unknown texts')
        # Applying SVM
        max_abs_scaler = preprocessing.MaxAbsScaler()
        scaled_train_data = max_abs_scaler.fit_transform(train_data)
        scaled_test_data = max_abs_scaler.transform(test_data)
        clf=CalibratedClassifierCV(OneVsRestClassifier(SVC(C=1)))
        clf.fit(scaled_train_data, train_labels)
        predictions=clf.predict(scaled_test_data)
        proba=clf.predict_proba(scaled_test_data)
        # Reject option (used in open-set cases)
        count=0
        for i,p in enumerate(predictions):
            sproba=sorted(proba[i],reverse=True)
            if sproba[0]-sproba[1]<pt:
                predictions[i]=u'<UNK>'
                count=count+1
        print('\t',count,'texts left unattributed')
        # Saving output data
        out_data=[]
        unk_filelist = glob.glob(path+os.sep+problem+os.sep+unk_folder+os.sep+'*.txt')
        pathlen=len(path+os.sep+problem+os.sep+unk_folder+os.sep)
        for i,v in enumerate(predictions):
            out_data.append({'unknown-text': unk_filelist[i][pathlen:], 'predicted-author': v})
        print(len(unk_filelist))
        print(len(out_data))
        print(unk_filelist[0])
        print(out_data[0])
        '''
        pathlib2.Path(outpath).mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(data=proba)
        df.to_csv(outpath+os.sep+'probs-'+problem+'.csv', sep=',', header=False, index=False)
        df = pd.DataFrame(data=clf.classes_)
        df.to_csv(outpath+os.sep+'classes-'+problem+'.csv', sep=',', header=False, index=False)
        
        with open(outpath+os.sep+'answers-'+problem+'.json', 'w') as f:
            json.dump(out_data, f, indent=4)
        print('\t', 'answers saved to file','answers-'+problem+'.json')'''
    print('elapsed time:', time.time() - start_time)


def main():
    parser = argparse.ArgumentParser(description='PAN-19 Baseline Authorship Attribution Method')
    parser.add_argument('-i', type=str, help='Path to the main folder of a collection of attribution problems')
    parser.add_argument('-o', type=str, help='Path to an output folder')
    parser.add_argument('-n', type=int, default=3, help='n-gram order (default=3)')
    parser.add_argument('-ft', type=int, default=5, help='frequency threshold (default=5)')
    parser.add_argument('-pt', type=float, default=0.1, help='probability threshold for the reject option (default=0.1')
    parser.add_argument('-typ', type=str, default='regular', help='type of ngram to use {regular, punct, struct} (default=regular')
    args = parser.parse_args()
    if not args.i:
        print('ERROR: The input folder is required')
        parser.exit(1)
    if not args.o:
        print('ERROR: The output folder is required')
        parser.exit(1)
    
    
    output_folder = args.o+os.sep+args.typ+os.sep+str(args.n)+os.sep+str(args.pt)
    print('output folder:  '+output_folder+'\n')
    
    # execute methods
    baseline(args.i, output_folder, args.n, args.ft, args.pt, args.typ)
    evaluate_all(args.i, output_folder, output_folder)
    update_results(args.o,args.typ,args.n,args.pt,args.ft)
    #write_probs(probs, pr)

def run_exhaustive(i, o, typ, ft):
    min_ngram = 2
    max_ngram = 9
    min_pt = 0.01
    max_pt = 0.02
    incr_pt = 0.01
    
    for ngram in range(min_ngram, max_ngram,1):
        for pt in arange(min_pt, max_pt, incr_pt):
            # create output folder
            output_folder = o+os.sep+typ+os.sep+str(ngram)+os.sep+str(pt)
            print('output folder:  '+output_folder+'\n')
            # execute methods
            baseline(i, output_folder, ngram, ft, pt, typ)
            evaluate_all(i, output_folder, output_folder)
            update_results(o, typ, ngram, pt, ft)

def meta_run(i, o, ft):
    methods = ''' punct_punct
                            punct_whitesp
                            punct_acc
                            punct_vow
                            punct_cons
                            punct_up
                            punct_acc_vow_up
                            vow
                            vow_star
                            vow_whit
                            struct_len_word
                            struct_len_sent
                            struct_range_word_2
                            struct_range_word_3
                            struct_range_word_4
                            struct_range_word_5
                            struct_range_sent_word_3
                            struct_range_sent_char_5
                            regular
                            reg_low'''
    
    for meth in word_methods:
    #for meth in methods.split('\n'):
        meth = meth.strip()
        print('Run exhaustive in method '+meth)
        run_exhaustive(i, o, meth, ft)

if __name__ == '__main__':
    #main()
    #meta_run("src\\pan19_CDAA_trainingDataset", "src\\results_countVec", 5)
    run_exhaustive("src"+os.sep+"pan19_CDAA_trainingDataset", "src\\results_countVec", 'end_punct', 5)
    

  
    
