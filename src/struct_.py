# -*- coding: utf-8 -*-
from nltk import word_tokenize as nltk_word_tokenize
from nltk import sent_tokenize as  nltk_sent_tokenize

def length_sent_by_words(text):
    sentences = nltk_sent_tokenize(text)
    new_txt = ''
    
    for sent in sentences:
        tokens = nltk_word_tokenize(sent)
        size_sent = len(tokens)
        if size_sent > 15:
            new_txt += '*'
        else:
            new_txt += hex(size_sent)[2:]
            
    return new_txt

def range_sent_by_words_3(text):
    sentences = nltk_sent_tokenize(text)
    new_txt = ''
    
    for sent in sentences:
        tokens = nltk_word_tokenize(sent)
        size_sent = len(tokens)
        if size_sent <= 10:
            new_txt += 's'
        elif size_sent <= 20:
            new_txt += 'm'
        else:
            new_txt += 'l'
            
    return new_txt

def range_sent_by_chars_5(text):
    sentences = nltk_sent_tokenize(text)
    new_txt = ''
    
    for sent in sentences:
        size_sent = len(sent)
        if size_sent <= 20:
            new_txt += 's'
        elif size_sent <= 50:
            new_txt += 'm'
        elif size_sent < 100:
            new_txt += 'r'
        elif size_sent < 200:
            new_txt += 'l'
        else:
            new_txt += 'h'

    return new_txt
    
def length_words(text):
    tokens = nltk_word_tokenize(text)
    new_txt = ''
    
    for tok in tokens:
        size_tok = len(tok)
        if size_tok > 15:
            new_txt += '*'
        else:
            new_txt += hex(size_tok)[2:]
    
    return new_txt

def range_words_2(text):
    tokens = nltk_word_tokenize(text)
    new_txt = ''
    
    for tok in tokens:
        size_tok = len(tok)
        if size_tok <= 5:
            new_txt += 's'
        else:
            new_txt += 'l'
    
    return new_txt

def range_words_3(text):
    tokens = nltk_word_tokenize(text)
    new_txt = ''
    
    for tok in tokens:
        size_tok = len(tok)
        if size_tok <= 3:
            new_txt += 's'
        elif size_tok >= 8:
            new_txt += 'l'
        else:
            new_txt += 'm'
    
    return new_txt

def range_words_4(text):
    tokens = nltk_word_tokenize(text)
    new_txt = ''
    
    for tok in tokens:
        size_tok = len(tok)
        if size_tok < 3:
            new_txt += 's'
        elif size_tok < 6:
            new_txt += 'm'
        elif size_tok < 9:
            new_txt += 'l'
        else:
            new_txt += 'h'
    
    return new_txt

def range_words_5(text):
    tokens = nltk_word_tokenize(text)
    new_txt = ''
    
    for tok in tokens:
        size_tok = len(tok)
        if size_tok < 3:
            new_txt += 's'
        elif size_tok < 5:
            new_txt += 'm'
        elif size_tok < 7:
            new_txt += 'r'
        elif size_tok < 9:
            new_txt += 'l'
        else:
            new_txt += 'h'
    
    return new_txt

text = ''''t speak to anyone. I saw her at the funeral, and she said a few words, but that's it. I went to see her afterwards, to pick up your stuff – they let me have it after the forensic team did their thing. Don't worry – Anderson wasn't allowed anywhere near your things. Anyway, Molly insisted staying with you all the while. I think she even slept at the mortuary at some point. You really didn't appreciate her enough. I heard from Lestrade that she doesn't let anyone look at your body if she is not present.

Lestrade called the other day, asking me to help out on a case. You would've been proud – I yelled at him for not doing his job and being an idiot. I haven't talked to him since.

You would have liked the case – supposedly murdered man in a stranger woman's house, doors and windows locked from the inside, no body and no woman present. Figured it out yet?

They actually found the victim two days ago. It was in the papers. It took them ten days. It turns out that there actually was a body, and it was hidden in some sort of an old tunnel under the house along with the killer.

The killer had died of blood-loss after the victim stabbed him with a kitchen knife. The killer (he hadn't really gotten around to killing anybody, but I guess he did kill, in a way) had fallen on top of the victim and she couldn't get out from under him, so she died of dehydration. It must have been torture, to have had died such a slow, painful death.

She had suffered from Amyotrophic Lateral Sclerosis and her carer was out of town visiting her sick daughter. The killer was the carer's daughter's biological father, who was schizophrenic but was diagnosed only three years after he donated his sperm. He mistook the victim for the carer and dragged her into the hidden tunnel and tried to rape her. There are no living witnesses to question, but the police think he didn't notice the knife (it was a rather large knife) because of his illness. His flat-mate said that he sometimes skipped his medicine and he had to remind him, but he forgot to a couple of days before the incident.

I can't help but think that if you were still alive you would have solved it in minutes, and the victim would still be alive. Even if it had taken you three days, she would still be alive.


Do you see what you've done? You selfish bastard. You didn't kill only yourself, but also all of


I don't know why Ella told me to write this. It's not like it would make any difference. You'd still be dead. It's not like it's helping, either. It's just making me feel a whole lot worse.

I don't know what your brother's doing. There have been more political resignations and even one murder – police think it's natural causes, but Mike told me that Molly's started juggling around with a lot of undetectable poisons like the one Moriarty had used to kill Carl Powers. Also, I've found some old article where the deceased had said, and I quote, 'I have seen how the government works, and I, like you, would like to believe that everything works properly, but that is not the case, as certain people whose names I will not reveal seem to be under the belief that they can do whatever they want, use whatever governmental resources they can get their hands on for personal affairs.' Personally, I believe your someone might have taken that statement to heart. That is, if he had a I didn't believe that someone to be capable of carrying out such extreme actions, but who knows what he is up to. Your death might be affecting him more than you think. Thought.

On a different note, this letter is almost long enough to get Ella off my back so that means I'll soon get to go back to 'depressing over your death', as she put it. But she's wrong. Depressed people don't do much of anything. I do things. I had tea with Mrs. Hudson, and I talked to Sarah yesterday.

And I talk to your skull. Not always, just when I want to talk without having someone talk back. And the skull doesn't talk back. I've checked. I'm curious, though, when you were still using did it seem like the skull was talking? No, sorry, that was rude. Ignore that. Well, don't. You need to hear this. It's good for you. That's what Ella said. You need to admit that you're not really 'fine, thank you'.

God, I'm writing to a dead man. At least you can't talk back.'''

#print(range_sent_by_words_3(text))