# -*- coding: utf-8 -*-
from util import str_as_set
from string import punctuation, whitespace, ascii_letters, digits
#‘
punctuation += '«’–¨¸—‘¡“¿”»…'
accents = 'áéíóúàèìòùâêîôûäëïöüÿæœçñ'
consonants = 'bcdfghjklmnpqrstvwxzçñ'
vowels = 'aeiouyáéíóúàèìòùâêîôûäëïöüÿæœ'

def get_all(text):
    return punct(text)+whitesp(text)+acc(text)

def trans_rare(text):
    set_common = str_as_set(ascii_letters+digits+whitespace+punctuation+accents)
    new_txt = '' 
    for ch in text.lower():
        if ch in set_common:
            new_txt += ch
        else:
            #print('this is weird -'+ch+'-')
            new_txt += 'Ø'
    return new_txt

def rare(text):
    return text.lower().translate(str.maketrans('', '', ascii_letters+digits+whitespace+punctuation+accents))

def punct(text):
    return trans_rare(text.lower()).translate(str.maketrans('', '', ascii_letters+digits+whitespace+accents))

def whitesp(text):
    return trans_rare(text.lower()).translate(str.maketrans('\n', 'n', ascii_letters+digits+punctuation+accents))

def acc(text):
    return trans_rare(text.lower()).translate(str.maketrans('', '', ascii_letters+digits+whitespace+punctuation))

def vow(text):
    return trans_rare(text.lower()).translate(str.maketrans('', '', consonants+digits+whitespace+punctuation))

def cons(text):
    return trans_rare(text.lower()).translate(str.maketrans('', '', vowels+digits+whitespace+punctuation))

def up(text):
    old = vowels+consonants+vowels.upper()+consonants.upper()
    new = ('l' * (len(vowels) + len(consonants)))+('u' * (len(vowels) + len(consonants)))
    return text.translate(str.maketrans(old, new, digits+whitespace+punctuation+rare(text)))

def acc_vow_up(text):
    text = text.translate(str.maketrans('', '', digits+whitespace+punctuation+rare(text)))
    set_acc = str_as_set(accents)
    set_vow = str_as_set(vowels)
    new_txt = '' 

    for ch in text:
        is_up = ch.isupper()
        is_acc = ch in set_acc
        is_vow = ch in set_vow
        
        if is_up and is_acc and is_vow: # Á
            new_txt += '1'
        elif is_up and is_acc and not is_vow: # Ñ
            new_txt += '2'
        elif is_up and not is_acc and is_vow: # A
            new_txt += '3'
        elif is_up and not is_acc and not is_vow: # N
            new_txt += '4'
        elif not is_up and is_acc and is_vow: # á
            new_txt += '5'
        elif not is_up and is_acc and not is_vow: # ñ
            new_txt += '6'
        elif not is_up and not is_acc and is_vow: # a
            new_txt += '7'
        elif not is_up and not is_acc and not is_vow: # n
            new_txt += '8'

    return new_txt

def punct_with_whitesp(text):
    new_txt = ''
    set_punct_whitesp = str_as_set(punctuation+'¡¿«—»'+whitespace)
    set_unused = str_as_set(ascii_letters+digits)
    
    for ch in text.lower():
        
        if ch in set_punct_whitesp:
            new_txt += ch
        elif ch not in set_unused:
            new_txt += 'x'
    
def extract_punct(text):
    new_txt = ''
    set_punct = str_as_set(punctuation+whitespace+'¡¿')
    set_punct = str_as_set(punctuation+'¡¿«—»')
    set_acc_0 = str_as_set(ascii_letters+digits)
    set_acc_1 = str_as_set('áéíóú') 
    set_acc_2 = str_as_set('àèìòù')
    set_acc_3 = str_as_set('âêîôû')
    set_acc_4 = str_as_set('äëïöü')
    set_acc_5 = str_as_set('ñ')
    set_acc_6 = str_as_set('ç')
    set_vowels = str_as_set('aeiouáéíóúàèìòùâêîôûäëïöü')
    
    for ch in text.lower():
        
        if ch in set_punct:
            new_txt += ch
        else:
            
            if ch in set_acc_1:
                new_txt += '´'
            if ch in set_acc_2:
                new_txt += '`'
            if ch in set_acc_3:
                new_txt += '^'
            if ch in set_acc_4:
                new_txt += '¨'
            if ch in set_acc_5:
                new_txt += '�'
            if ch in set_acc_6:
                new_txt += '¸'
            
       
        '''    if not ch in set_acc_0:
                new_txt += 'N'
        '''     
    '''
    print(punctuation)
    print(text)'''
    #print(new_txt)
    
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

God, I'm writing to a dead man. At least you can't talk back.
'''
'''
print('EN')
print(punct(text))
print(whitesp(text))
print(acc(text))
print(rare(text))
print(vow(text))
print(cons(text))
print(up(text))
print(acc_vow_up(text))
'''
text = '''lui – qu'il lui fasse mal, sans le savoir. Parce que ça blessait Castiel d'être conscient que Dean n'avait plus besoin de lui. Il ne pouvait pas ne pas éprouver une pointe de rancœur à l'idée que Dean l'avait laissé tomber, ainsi que tout le reste. Comme s'il était une voiture qu'on mettait au garage et qu'on recouvrait soigneusement d'une bâche pour ne plus y penser.Il ne l'aurait pas avoué, mais il aimait quand Dean avait besoin de lui. Cela lui donnait une bonne excuse pour rester à ses côtés et l'aimer sans rien dire.

Lorsqu'il entendit son nom être appelé, tous ses doutes s'évaporèrent, comme un envol dispersé de moineaux. Il fonça sans réfléchir auprès de son protégé, rempli d'appréhension : si Dean lui demandait de l'aide, c'était peut-être qu'il était en danger. Il aurait dû s'y attendre. Il aurait dû le protéger. C'était son rôle après tout.Il se fustigea de ne pas avoir gardé un œil sur lui. Il était si fragile, désormais, sans Sam, sans aucun ange à ses côtés ; et comment avait-il pu imaginer un seul instant que les monstres laisseraient Dean tranquille ?Une partie de lui, cependant, une toute petite partie de lui criait victoire. Il essayait vainement de la faire taire en se rendant dans la maison qu'habitait Dean.



Il avait eu tort de s'inquiéter. Dean allait très bien. Il dormait dans le lit de sa compagne, toujours tourné vers la porte, un bras pendant dans le vide, près à saisir la crosse du flingue qui reposait sur la table de chevet vide.Cependant son sommeil était agité. D'un coup d’œil, Castiel savait qu'il faisait un cauchemar. Il l'avait déjà observé maintes et maintes fois. Ses traits tendus, la sueur froide coulant dans sa nuque, et le gémissement bas sortant de sa bouche, comme une prière...« Cas...Cas !... »L'ange pencha la tête sur le côté, ses lèvres frémissant d'un sourire contenu. Ce garçon était à ses yeux plus précieux que l'univers tout entier. Et il appelait son nom dans son sommeil.Ça remplissait sa poitrine d'une sensation étrange ; une boule de chaleur irradiait ses côtes et pressait son cœur comme un citron. C'était agréable et douloureux à la fois.Il tendit deux doigts vers le front plissé du jeune homme pour chasser le mauvais rêve, lorsque celui-ci ouvrit brusquement les yeux.Castiel fut pétrifié sur l'instant, transpercé par ses yeux verts tant aimés, avant de se souvenir qu'il ne pouvait pas le voir. Le regard de Dean fixa le vide quelques secondes, un peu trop brillant, un peu trop torturé pour que Cas put le soutenir plus longtemps.Le chasseur se frotta les paupières en soupirant.- Dean ?La jeune femme dans son dos se redressa et posa la main sur son épaule.- Ça va ?Dean se retourna et lui prit la main. Sa voix retentit dans l'obscurité, douce et rocailleuse, empli d'une tendresse sourde qui rendit Castiel jaloux.Il se rendit compte qu'il ne l'avait pas entendu depuis des lustres. Qu'elle lui avait manqué, comme tout ce qui le concernait.Il lui manquait tellement.- Juste un cauchemar. Rendors-toi.Un bras fin jaillit de sous la couverture et entoura les épaules de Dean.- Viens par là, chuchota Lisa avec affection.Castiel les regarda s'embrasser avec une boule au ventre. Il ne devrait pas être là.Mais il était fasciné par le mouvement de leurs corps entrelacés, par la langueur de leurs gestes alourdis de sommeil. Il détailla les muscles du dos de Dean lorsque celui-ci se coucha sur sa partenaire, bougeant lentement contre elle, le drap couvrant à peine sa chute de rein et l'arrondi de ses fesses.Leurs souffles haletants envahirent le silence de la chambre, et Castiel se sentit de plus en plus mal à l'aise. Ce n'était pourtant pas la première fois qu'il voyait des humains copuler.Pourtant ce n'était pas pareil. Ce n'était pas n'importe quels humains.C'était Dean.Son corps hâlé suivait une ondulation sensuelle qui envoyait des étincelles pétiller le long de la colonne vertébrale de l'observateur, hérissant le duvet de la nuque. Il se mordit l'intérieur de la joue pour ne pas gémir tandis que la jeune femme ne se retenait pas, elle. Elle replia ses longues jambes graciles sur les hanches de son compagnon et lui griffa l'épaule, là où Castiel avait jadis apposé sa marque. Le lit trembla quand Dean atteignit l'orgasme en elle, renversant la tête en arrière dans un râle brut.Il ne lui fallut pas longtemps avant de retomber à ses côtés, épuisé.Castiel les contempla un moment, alors qu'ils échangeaient quelques caresses et baisers. Voilà ce dont Dean avait réellement besoin. D'amour et de confiance. De réconfort.D'une famille.
'''
'''
print('FR')
print(punct(text))
print(whitesp(text))
print(acc(text))
print(rare(text))
print(vow(text))
print(cons(text))
print(up(text))
print(acc_vow_up(text))
'''
text = '''fondo di una gola rovinata.
Io non trovai proprio niente di sensato da dirgli. Quando mi  sussurrò: ‘Speriamo che non salti il tour,’ me ne uscii con il solito: ‘Scherzi?’
Aveva solo il raffreddore. Per me. Per tutti. Persino per  l’egoismo di chi diceva di amarlo per prendere e basta. Per pretendere un  eroismo da foglio di carta.
Era così piccolo, Bill. Aveva solo diciotto anni.
Diciotto anni di sogni e di parole e di niente.  Improvvisamente di niente.
Speriamo che non sia qualcosa di grave. ‘Scherzi?’  
È curioso, credevo di essere un tipo molto coraggioso.  Credevo che per tutta la vita sarei stato il sostegno di mio fratello. Bill  aveva bisogno di me. Chiaro, no?
Invece ero quello più spaventato di tutti. Ero quello che,  davanti all’evidenza, preferiva pensare a un brutto scherzo. A uno scherzo del  cazzo, ma a uno scherzo.
Quando ci ritrovammo a Hamburg, Bill non parlava quasi più  per niente.
Tra noi non ce n’era mai stato un gran bisogno, ma era innaturale.
Il suo silenzio. I miei silenzi.
Non avevo nulla da dirgli. Niente di niente.
Volevo che qualcuno mi battesse sulla spalla e mi dicesse: ‘D’accordo.  Abbiamo giocato un po’. Adesso basta.’
Fu proprio come svegliarsi da un sogno luminoso; qualcosa di  tanto realistico e netto e vivido che separartene ti procura un dolore  viscerale, tant’è che per un po’ stai lì a chiederti quale sia il sogno e quale  sia invece la realtà.
Bill mi guardava e credo che mi leggesse dentro: la mia  incredulità vigliacca e un po’ egoista. La mia paura. La mia incertezza.
Non parlava più, però ebbe il coraggio di dirmelo lo stesso;  di raccogliere quel po’ di voce che aveva messo da parte per spenderla solo per  me.
C’è una cisti, Tomi. Devono toglierla. Scherzi?  
Aveva paura, Bill, ma sorrideva lo stesso. Si dava un tono.  Aveva diciotto anni e, chissà? Ci sperava?
Aveva combattuto così tanto per i propri sogni ch’era  innaturale pensare che potesse perdere. Non lui. Non davvero uno del genere.
La mia voce tremava, quando mi toccò dare quell’annuncio. A  me, proprio a me: a me per cui era tutto.
Ed era una sensazione atroce e straniante insieme. Una  settimana prima, più o meno, me l’ero fatta addosso per parargli il culo da un  raffreddore – già. Solo un raffreddore. Ora dovevo dire che era qualcos’altro –  qualcosa di sbagliato. Qualcosa che avrebbe forse cambiato per sempre la voce di  Bill.
Come sarebbe stata?
Per un po’ non avrei riconosciuto mio fratello. Suonava  strano.
Gli stringevo piano la mano e dividevo con lui quella  stronzata che, all’improvviso, mi sembrava rilevantissima.
Le dita di Bill erano calde e sottili. Le sue unghie erano  trasparenti. Erano bellissime.
In ospedale non poteva portare lo smalto. La mia attenzione  si fossilizzava su dettagli da niente.
Forse mi stavo svegliando anch’io; lo stavo raggiungendo  oltre il bordo scheggiato del suo sogno. Precedendomi, però, mio fratello faceva  ancora il possibile per impedirmi di tagliarmi.
Per proteggermi. Per rassicurarmi.
Aveva paura, ma non voleva dividerla con me.
La sua stanza sembrava un bunker o un negozio di giocattoli.  L’avevamo riempito di regali.
Gli avevo comprato una scimmia di peluche ch’era due volte  lui. L’avevo fatto perché non si sentisse solo quando non c’ero. Io ero una  scimmia. Ero la sua scimmia.
Non potevo comprargli il coraggio. Non potevo comprargli la  salute.
Tutto il mio potere si esauriva in qualcosa di tanto stupido  come un giocattolo: a Bill faceva piacere lo stesso.
Poco prima che lo portassero via, per prepararlo  all’intervento, ho avuto l’impressione che volesse chiedermi scusa. Scherzi?  
Non aveva colpa di niente, proprio di niente: mi aveva fatto  solo un po’ di posto al suo fianco.
Ci avevano assicurato che l’operazione sarebbe durata al più  un’ora e mezza – due, a dire tanto. Non era nulla di complicato. Era routine.  Sarebbe andato tutto bene.
Dopo tre ore, nessuno ci aveva ancora detto niente.
Io avvertivo quel silenzio scivolare in me e trascinare via  tutto il coraggio.
Avevo voglia di svegliarmi, ora: solo che l’avevo già fatto.
La cisti non era una cisti. Era un tumore. Un cancro. Una  sacchettina di merda. Scherzi?
No. E tagliare non bastava più. Bisognava raschiare tutt’intorno.  Fare piazza pulita.
Tutt’intorno. Scherzi?
No. Non avremmo più sentito la sua voce. Cristo, stai scherzando?
No.
Ero inebetito. Se Bill l’avesse saputo, forse avrebbe  preferito morire. Sul palco, magari. Sotto le luci. Spegnersi con la sua voce,  poco a poco.
La sua voce che già non ricordavo quasi più, che avrei  dimenticato per sempre.
La sua voce ch’era anche la mia, perché mi aveva sempre  guidato, in qualche modo.
Era fuori ed era dentro di me, come uno stimolo o come una  preghiera
'''
'''
print('IT')
print(punct(text))
print(whitesp(text))
print(acc(text))
print(rare(text))
print(vow(text))
print(cons(text))
print(up(text))
print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
print(acc_vow_up(text))
'''
text = '''por todo su cuerpo peor que cualquier tortura.

Estaba agonizando de hambre y no podía dejar pasar un solo segundo más. Era la muestra clara de esos ojos hundidos en un negro total, con sus iris sangrientas rodeando las pupilas que se contraían y dilataban sin control a través del vidrio de sus anteojos.

Kei gruñó y separó sus mandíbulas mostrando sus letales colmillos junto a los hilos e hilos de saliva que le chorreaban por el mentón. Su cabeza palpitaba igual de acelerado que los latidos de la mujer y se lanzó contra ella cuando entonces su sollozo lo detuvo de golpe a escasos milímetros.

La chica tenía los ojos apretados y el rostro ladeado contra el sucio piso, levantando el polvo con la fuerte respiración que salía por su nariz y boca. Tembló entera cuando sintió la lengua del Ghoul arrastrándose por la herida de su sien que se hizo al caer con el monstruo encima, y repitió lo que había hecho que el rubio se detuviera.

— P- po- por favor, no lo hagas… —buscó el coraje suficiente para lograr abrir sus ojos inundados en lágrimas y mirarlo, buscando compasión— Estoy… estoy embarazada.

La mirada de Kei flaqueó y por un momento pareció que su mente estaba de vuelta. El fondo negro de su ojo derecho había empezado a desvanecerse lentamente cuando el ruido de unos zapatos de cuero vino del fondo del callejón tras de él. Los pasos se detuvieron y la mujer lo vio parado por encima del rubio, con esa misma sonrisa que parecía burlarse de las vidas ajenas.

— La comida no debería hablar. No la escuches, Tsukki.

— … Yo… no.

— Shhh. —Kuroo se inclinó tras su espalda y le pasó una mano por la cintura arrastrándola hasta su abdomen, donde encajó la punta de sus dedos— Si tienes hambre, simplemente come.

Estuvo en sus cálculos que la parte humana de Kei tratara de retomar el control. Un Ghoul hermoso nacido de un padre come-gente y una mujer humana, y fue criado por ella para que pudiese coexistir con las personas, como uno más de ellos, sobreviviendo con partes de cadáveres que nadie extrañaría.

Pero eso no era lo más relevante del resultado de esta unión antinatural. Kei había logrado desarrollar un gusto por un alimento en específico aparte del café, y no era un gusto a excremento como le sabía a los Ghouls la comida de los humanos, no. No sólo podía olfatear el rico aroma de las tartas sino que al saborearlas podía masticar y empujarlo por su garganta con el mayor gusto del mundo, porque le sabía delicioso.

Al principio su cuerpo lo rechazaba y terminaba vomitándolo pero acabó por acostumbrarse sin que su organismo sufriera daños. Kei quiso aferrarse a esto como su sueño de ser un humano normal, sin embargo era imposible que viviera de ello. Luego de tres semanas sin alimentarse como Ghoul comenzaban las ansias, los dolores de cabeza, se volvía más débil e iba en deterioro.

Su límite eran 33 días, después de ese tiempo en abstinencia las tartas y pequeñas transfusiones sanguíneas no servían de nada. Y esta vez, en su día 35 enloqueció. Finalmente su estómago había sacado sus propias garras raspándole por dentro, pidiendo carne, carne con la sangre y la grasa que necesitaba para vivir, la carne que sólo podía ofrecerle un humano.

Kuroo lo guió a su primera caza en la que obtuvo a esta chica con apariencia sana, no parecía enferma y no estaba demasiado delgada. La cena perfecta. No era muy difícil y Kei se podría adaptar, no importaba si lo odiaba cuando al día siguiente recobrara el conocimiento.


Sabes que lo hago por ti.


— Come, Tsukki.

— ¡¡Noo!! ¡No me comas! Mi bebé, ¡… tengo un niño aquí! —se llevó la mano a su vientre tanteando con la otra por el suelo, desesperada y sin parar de llorar rogándole a Kei.

El chico estaba en shock, paralizado, con la parte negra de su ojo luchando por dominar el color blanco humano que quería irrumpir. El pelinegro apretó sus labios en torno a la oreja de Kei bordeando su forma desde el cartílago hasta el lóbulo donde acabó con una lamida, estiró una sonrisa que mostraba todos sus dientes y susurró mirando a la mujer con sus propios ojos de Ghoul.

— Es mentira.

Logró alcanzar una botella de vidrio que había caído de una bolsa de basura y gritando con todas sus fuerzas atacó a Kei con ella. Sin embargo fue menos que inútil cuando el kagune del rubio floreció y le atravesó el brazo clavándolo en el concreto, e hizo lo mismo con el otro arrancándole unos increíbles sonidos de sufrimiento.

Maravilloso. Su forma, la combinación de colores que latían en cada trazo, su fuerza letal, un kagune tan bello y majestuoso como plumas filosas sólo podía confirmar la existencia de Dios, un dios que había colocado a los Ghouls en la cima de la cadena alimenticia.

Kuroo gimió viendo como los instintos de Kei se expresaban como arte, impulsando al menor a desbaratarle la ropa y clavar sus dientes atravesando el abdomen de la mujer para luego echar su cabeza hacia atrás y arrancarle el pedazo de carne de una forma brutal. El pelinegro metió sus dedos en la boca de la chica para acallar sus escandalosos y tontos chillidos que no servirían de nada, mientras estaba
'''
'''
print('ES')
print(punct(text))
print(whitesp(text))
print(acc(text))
print(rare(text))
print(vow(text))
print(cons(text))
print(up(text))
print(acc_vow_up(text))
'''