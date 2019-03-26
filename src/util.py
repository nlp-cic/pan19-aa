# -*- coding: utf-8 -*-
import pandas as pd
import os
from os import sep as os_sep
from os.path import exists as os_exists
from json import load as json_load
from json import dump as json_dump

def write_probs(probs, outpath):
    for i in enumerate(len(probs)):
        df = pd.DataFrame(data=probs[i])
        df.to_csv(outpath+os.sep+'probs-'+i+'.csv', sep=' ', header=False, index=False)
    
def str_as_set(str_in):
    set_out = set()
    for ch in str_in:
        set_out.add(ch)
        
    return set_out

def empty_call(text):
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
 
def update_results(o,typ,n,pt,ft,output_folder, probs):
    # extract current score
    current_value = get_score(output_folder)
    
    # check if current result it is best than best results per level
    paths_results = [o, o+os_sep+typ, output_folder]
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
            
            write_probs(probs, pr)
            
            if pr == o:
                print('New best result: '+str(current_value))