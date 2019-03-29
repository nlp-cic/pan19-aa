# -*- coding: utf-8 -*-
from util import str_as_set
from string import whitespace, ascii_letters

def get_sets():
    set_vowels = str_as_set('aeiouáéíóúàèìòùâêîôûäëïöüœ')
    set_letters = str_as_set(ascii_letters+'ñç')
    return set_vowels, set_letters

def vowels(text):
    
    set_vowels, set_letters = get_sets()
    new_txt = ''
    
    for ch in text.lower():
        if ch in set_vowels:
            new_txt += 'v'
        elif ch in set_letters:
            new_txt += 'c'

    return new_txt

def vowels_with_stars(text):
    
    set_vowels, set_letters = get_sets()
    new_txt = ''
    
    for ch in text.lower():
        if ch in set_vowels:
            new_txt += 'v'
        elif ch in set_letters:
            new_txt += 'c'
        else:
            new_txt += '*'
            
    return new_txt
# insignificante
def vowels_with_withesp(text):
    
    set_vowels, set_letters = get_sets()
    set_whitesp = str_as_set(whitespace)
    
    new_txt = ''
    for ch in text.lower():
        if ch in set_vowels:
            new_txt += 'v'
        elif ch in set_letters:
            new_txt += 'c'
        elif ch in set_whitesp:
            new_txt += ' '
        else:
            new_txt += '*'

    return new_txt

