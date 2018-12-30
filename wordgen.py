import random 
import sys
import itertools

consonants = []
vowels = []
dipthongs = []
vowels_and_dipthongs = []
codas = []
coda_clusters = [[]]
onset_clusters = [[]]
syllable_structures = []

help_text = '''
This program uses a phonetics.csv file to defined the ponetic rules of the language for which to generate words. This phoneitcs file should have the following elements:
\tconsonants,<consonants>
\tvowels,<vowels>
\tdipthongs,<dipthongs>
\tcodas,<codas>
\tcoda_clusters,<coda_clusters>
\tonset_clusters,<onset_clusters>
\tsyllable_structures,<syllable_structures>
\tuse # to comment out a line--the whole line is ignored  regarless of there # is placed!
\tex
\t\t#Basic sounds
\t\tconsonants,fvszptjwlrhtdmn
\t\tvowels,aeiou
\t\tdipthongs,ai,eu

\t\t#clusters and codas
\t\tcodas,szf
\t\tcoda_clusters,st,rl
\t\tonset_clusters,ts,lr,dz

\t\t#syllable structure patterns
\t\tsyllable_structures,v,cv,cvc,ccvc,ccvcc,cvcc


usage form: python wordgen.py <*num_words> <*num_syllables_per_word> <*phonotactics_file> <output_file> <allow_clusters> <allow_dipthongs> <allow_codas> <allow_onsets> <allow_repeats>
elements marked with an asterisk are required to run the program, the rest are optional customizations
\t<num_words> is the number of words to generate. Enter 0 to generate all possible words (no repeats)
\t<num_syllables_per_word> is the number of syllables each word will have
\ty<phonotactics_file> type -in:FILE_NAME to specify the file containing phonotactic data for word generation
\t<output_file> type -out:FILE_NAME to specify an output file. If none is given words will be printed to the terminal
\t<allow_clusters> type -nocluster to indicate that no consonant clusters are allowed
\t<allow_dipthongs> type -nodip to indicate that no dipthongs are allowed
\t<allow_codas> type -nocoda to ban coda consonants
\t<allow_onsets> type -noonset to ban onset consonants
\t<allow_repeats> type -noreps to ban repeat word generation
\tex:
\t\tpython wordgen.py 50 2 -nocluster
\t\tpython wordgen.py 23 3 -nodip
\t\tpython wordgen.py 16 1
\t\tpython wordgen.py 38 4 -nocluster -nodip
'''

def loadData():
    for element in sys.argv:
        if '-in:' in element:
            useless, out_file = element.split(':', 2)
    try:
        with open('phonetics.csv', 'r', encoding='utf8') as phoneticsFile:
            phonetics = phoneticsFile.readlines()
            for line in phonetics:
                #ignore commented regions
                if '#' in line:
                    continue

                #ignore blank or corrupt lines
                try:
                    key, value = line.split(',', 1)
                except:
                    continue

                #remove whitespace from the data
                value = value.strip()

                #vowel types
                if key == 'vowels':
                    for vowel in value:
                        vowels.append(vowel)
                elif key == 'dipthongs':
                    dipthong_set = value.split(',')
                    for dipthong in dipthong_set:
                        dipthongs.append(dipthong[0] + dipthong[1])

                #consonant types
                elif key == 'consonants':
                    for consonant in value:
                        consonants.append(consonant)
                elif key == 'codas':
                    for coda in value:
                        codas.append(coda)
                elif key == 'coda_clusters':
                    cluster_set = value.split(',')
                    for cluster in cluster_set:
                        ipa_cluster = cluster
                        index = len(cluster) - 2
                        while index >= len(coda_clusters):
                            coda_clusters.append(list())
                        coda_clusters[index].append(ipa_cluster)
                elif key == 'onset_clusters':
                    cluster_set = value.split(',')
                    for cluster in cluster_set:
                        ipa_cluster = cluster
                        index = len(cluster) - 2
                        while index >= len(onset_clusters):
                            onset_clusters.append(list())
                        onset_clusters[index].append(ipa_cluster)

                #phonological data
                elif key == 'syllable_structures':
                    structure_set = value.split(',')
                    for s in structure_set:
                        syllable_structures.append(s)
                    
            vowels_and_dipthongs.extend(vowels + dipthongs)
    except:
        print('Phonetics file missing or invalidly formatted')
        exit()

def gen_all_words(num_syllables, no_cluster, no_dipthongs, no_onsets, no_codas):
    words = []
    
    #gen all possible single syllabkes
    syllables = []
    for syllable_structure in syllable_structures:
        syllables.extend(gen_all_syllables(syllable_structure, no_dipthongs))

    products = itertools.product(syllables, repeat = num_syllables)
    for product in products:
        word = str(product)
        word = word.replace("'", '')
        word = word.replace('(', '')
        word = word.replace(')', '')
        word = word.replace(',', '')
        word = word.replace(' ', '')
        words.append(word)

    return words

def gen_all_syllables(syllable_structure, no_dipthongs):
    v = syllable_structure.find('v')
    coda_num = len(syllable_structure) - 1 - v
    onset_set = []
    vowel_set = []
    coda_set = []
    syllables = []

    #beginning consonant(s)
    if v == 1:
        for i in range(len(consonants)):
            add_single_consonant(onset_set, i)
    elif v > 1:
        for i in range(len(onset_clusters)):
            add_onset_cluster(onset_set, v - 1 - 2, i)

    #vowel
    for i in range(len(vowels if no_dipthongs else vowels_and_dipthongs)):
        add_vowel(vowel_set, no_dipthongs, i)

    #coda consonant(s)
    if coda_num == 1:
        for i in range(len(codas)):
            add_single_coda(coda_set, i)
    elif coda_num > 1:
        for i in range(len(coda_clusters)):
            add_coda_cluster(coda_set, coda_num - 1 - 2)


    for onset in onset_set:
        for vowel in vowel_set:
            for coda in coda_set:
                syllable = onset + vowel + coda
                syllables.append(syllable)

    return syllables

def gen_words(num_words, num_syllables, no_cluster, no_dipthongs, no_onsets, no_codas, no_reps):
    words = []
    for i in range(num_words):
        next_word = ''
        while no_reps and next_word in words or next_word == '':
            next_word = gen_word(num_syllables, no_cluster, no_dipthongs, no_onsets, no_codas)
        words.append(next_word)
    return words

def gen_word(num_syllables, no_cluster, no_dipthongs, no_onsets, no_codas):
    word = ''
    for i in range(num_syllables):
        word += gen_syllable(no_cluster, no_dipthongs, no_onsets, no_codas)
    return word

def gen_syllable(no_cluster, no_dipthongs, no_onsets, no_codas):
    syllable_structure = syllable_structures[random.randint(0, len(syllable_structures) - 1)]
    v = syllable_structure.find('v')
    coda_num = len(syllable_structure) - 1 - v
    letter_set = []
    syllable = ''

    #prevent clusters is needed
    if no_cluster:
        while v > 1 or coda_num > 1:
            syllable_structure = syllable_structures[random.randint(0, len(syllable_structures) - 1)]
    
    #beginning consonant(s)
    if not no_onsets:
        if v == 1:
            add_single_consonant(letter_set)
        elif v > 1:
            add_onset_cluster(letter_set, v - 1 - 2)

    #vowel
    add_vowel(letter_set, no_dipthongs)

    #coda consonant(s)
    if not no_codas:
        if coda_num == 1:
            add_single_coda(letter_set)
        elif coda_num > 1:
            add_coda_cluster(letter_set, coda_num - 1 - 2)

    for letter in letter_set:
        syllable += letter

    return syllable

def add_vowel(letter_set, no_dipthongs, nth = -1):
    vowel = None
    if nth == -1:
        if no_dipthongs:
            nth = random.randint(0, len(vowels) - 1)
        else:
            nth = random.randint(0, len(vowels_and_dipthongs) - 1)
    if no_dipthongs:
        vowel = vowels[nth]
    else:
        vowel = vowels_and_dipthongs[nth]
    letter_set.append(vowel)

def add_single_consonant(letter_set, nth = -1):
    if nth == -1:
        nth = random.randint(0, len(consonants) - 1)
    consonant = consonants[nth]
    letter_set.append(consonant)

def add_single_coda(letter_set, nth = -1):
    if nth == -1:
        nth = random.randint(0, len(codas) - 1)
    coda = codas[nth]
    letter_set.append(coda)

def add_onset_cluster(letter_set, size, nth = -1):
    cluster_subset = onset_clusters[size]
    if nth == -1:
        nth = random.randint(0, len(cluster_subset) - 1)
    onset_cluster = cluster_subset[nth]
    letter_set.append(onset_cluster)

def add_coda_cluster(letter_set, size, nth = -1):
    cluster_subset = coda_clusters[size]
    if nth == -1:
        nth = random.randint(0, len(cluster_subset) - 1)
    coda_cluster = cluster_subset[nth]
    letter_set.append(coda_cluster)

def start_gen():
    #print help if no args given
    if len(sys.argv) < 3:
        print(help_text)
        exit()

    num_words = 0
    num_syllables = 0
    no_cluster = False
    no_dipthongs = False
    no_onsets = False
    no_codas = False
    no_reps = False
    out_file = None
    gen_all = False

    #Get user input
    try:
        num_words = int(sys.argv[1])
        if num_words == 0:
            gen_all = True
        if num_words < 0:
            raise ValueError('num_words may not be negative')
    except:
        print('please enter a non-negative integer number of words to generate')
        exit()

    try:
        num_syllables = int(sys.argv[2])
        if(num_syllables < 0):
            raise ValueError('num_syllables may not be negative')
    except:
        print('please enter a non-negative integer number of syllabes per word')
        exit()

    if '-nocluster' in sys.argv:
        no_cluster = True
    
    if '-nodip' in sys.argv:
        no_dipthongs = True

    if '-noonset' in sys.argv:
        no_onsets = True
    
    if '-nocoda' in sys.argv:
        no_codas = True

    if '-noreps' in sys.argv:
        no_reps = True

    for element in sys.argv:
        if '-out:' in element:
            useless, out_file = element.split(':', 2)

    #Generate words
    if gen_all:
        words = gen_all_words(num_syllables, no_cluster, no_dipthongs, no_onsets, no_codas)
    else:    
        words = gen_words(num_words, num_syllables, no_cluster, no_dipthongs, no_onsets, no_codas, no_reps)

    if out_file == None:
        for word in words:
            print(word)
    else:
        with open(out_file, 'w', encoding='utf8') as out:
            for word in words:
                print(word, file=out)

def main():
    loadData()
    start_gen()

main()