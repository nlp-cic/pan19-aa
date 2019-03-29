# -*- coding: utf-8 -*-
import os
import glob
import json
import pandas as pd
from os import sep as os_sep
from os.path import exists as os_exists
from json import load as json_load
from json import dump as json_dump

def str_as_set(str_in):
    set_out = set()
    for ch in str_in:
        set_out.add(ch)
        
    return set_out

def empty_call(text):
    print('ERROR: -typ argument is wrong')
    exit(1)
def empty_call2(text, size_grams, language):
    print('ERROR: -typ argument is wrong')
    exit(1)

def regular(text):
    return text

def reg_low(text):
    return text.lower()

def get_score(output_folder):
    
    result_file = output_folder+os_sep+'out.json'
    with open(result_file, 'r') as f:
        result_json = json_load(f)  
        current_value = result_json['overall_score']
    
    return current_value

def unify(methods, ngram_orders, pt, in_folder, out_folder):
    list_meth = methods.split('&')
    list_ngrs = ngram_orders.split('&')
    if len(list_meth) != len(list_ngrs):
        print('ERROR the number of methods and ngram orders must be the same')
        exit(1)
    
    infocollection = in_folder+os.sep+'collection-info.json'
    problems = []
    with open(infocollection, 'r') as f:
        for attrib in json.load(f):
            problems.append(attrib['problem-name'])
    for problem in problems:
        print(problem)
        # Reading information about the problem
        infoproblem = in_folder+os.sep+problem+os.sep+'problem-info.json'
        candidates = []
        with open(infoproblem, 'r') as f:
            fj = json.load(f)
            unk_folder = fj['unknown-folder']
            for attrib in fj['candidate-authors']:
                candidates.append(attrib['author-name'])
        
        out_data=[]
        unk_filelist = glob.glob(in_folder+os.sep+problem+os.sep+unk_folder+os.sep+'*.txt')
        pathlen=len(in_folder+os.sep+problem+os.sep+unk_folder+os.sep)
        
        for i,v in enumerate(unk_filelist):
            out_data.append(unk_filelist[i][pathlen:])
        print(unk_filelist[0])
        print(out_data[0])
        '''
        for i,v in enumerate(predictions):
            out_data.append({'unknown-text': unk_filelist[i][pathlen:], 'predicted-author': v})
        '''
        for i in range(len(list_meth)):
            path_method = 'results'+os.sep+list_meth[i]+os.sep+list_ngrs[i]
            if not os.path.exists(path_method):
                print(path_method+' doesnt exists')
                continue
            
            
        sum_scores = 0.0
unify('regular&punct_punct&vow_whit', '4&2&8', 0.1, "pan19_CDAA_trainingDataset", 'out_test')

'''    
    
    probs_problms = []
    # iterate over every method
    
    
    for i in range(len(list_meth)):
        path_method = 'results'+os.sep+list_meth[i]+os.sep+list_ngrs[i]
        if not os.path.exists(path_method):
            print(path_method+' doesnt exists')
            continue
        
        # get score for current method
        current_score = get_score(path_method)
        trunk_score = float('%.0f'%(current_score))
        sum_scores += trunk_score
        
        
        for j in range(1, 21):
            current_probs = pd.read_csv(path_method+os.sep+'probs-'+i+'.csv', header=0)
            if j > len(probs_problms):
                probs_problms.append(current_probs)
            else:
                for k in range(len(current_probs)):
                    for l in range(len(current_probs[0])):
                        probs_problms[j][k][l] += current_probs[k][l]

    ####################################################
    for i in range(20):
        for j in range(len(probs_problms[i])):
            for k in range(len(probs_problms[i][j])):
                probs_problms[i][j][k] = probs_problms[i][j][k]/20.0 
    '''
'''            count=0
            for i,p in enumerate(predictions):
                sproba=sorted(proba[i],reverse=True)
                if sproba[0]-sproba[1]<pt:
                    predictions[i]=u'<UNK>'
                    count=count+1
            print('\t',count,'texts left unattributed')
  '''

def update_results(o,typ,n,pt,ft):
    output_folder = o+os.sep+typ+os.sep+str(n)+os.sep+str(pt)
    # extract current score
    current_value = get_score(output_folder)
    
    # check if current result it is best than best results per level
    paths_results = [o, o+os_sep+typ, o+os.sep+typ+os.sep+str(n), output_folder]
    for pr in paths_results:
        if os_exists(pr+os_sep+'best_result'):
            with open(pr+os_sep+'best_result', 'r') as f:
                result_json = json_load(f)  
                best_value = result_json['best_score']
        else:    
            best_value = -1.0
            
        if current_value > best_value:
            with open(pr+os_sep+'best_result', 'w') as f:
                json_dump({'best_score':current_value,'typ':typ,'ngram':n,'pt':pt,'ft':ft}, f, indent=4)
            
            if pr == o:
                print('New best result: '+str(current_value))