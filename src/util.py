# -*- coding: utf-8 -*-
import os
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

def unify(methods, ngram_orders, pt, out_folder):
    list_meth = methods.split('&')
    list_ngrs = ngram_orders.split('&')
    if len(list_meth) != len(list_ngrs):
        print('ERROR the number of methods and ngram orders must be the same')
        exit(1)
    
    sum_scores = 0.0
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
            count=0
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