This program uses a phonetics.csv file to defined the phonetic rules of the language for which to generate words. This phonetics file should have the following elements:
        consonants,<consonants>
        vowels,<vowels>
        dipthongs,<dipthongs>
        codas,<codas>
        coda_clusters,<coda_clusters>
        onset_clusters,<onset_clusters>
        syllable_structures,<syllable_structures>
        use # to comment out a line--the whole line is ignored  regardless of there # is placed!
        ex
                #Basic sounds
                consonants,fvszptjwlrhtdmn
                vowels,aeiou
                dipthongs,ai,eu

                #clusters and codas
                codas,szf
                coda_clusters,st,rl
                onset_clusters,ts,lr,dz

                #syllable structure patterns
                syllable_structures,v,cv,cvc,ccvc,ccvcc,cvcc


usage form: python wordgen.py <*num_words> <*num_syllables_per_word> <*phonotactics_file> <output_file> <allow_clusters> <allow_dipthongs> <allow_codas> <allow_onsets> <allow_repeats>
elements marked with an asterisk are required to run the program, the rest are optional customizations
        <num_words> is the number of words to generate. Enter 0 to generate all possible words (no repeats)
        <num_syllables_per_word> is the number of syllables each word will have
        y<phonotactics_file> type -in:FILE_NAME to specify the file containing phonotactic data for word generation
        <output_file> type -out:FILE_NAME to specify an output file. If none is given words will be printed to the terminal
        <allow_clusters> type -nocluster to indicate that no consonant clusters are allowed
        <allow_dipthongs> type -nodip to indicate that no dipthongs are allowed
        <allow_codas> type -nocoda to ban coda consonants
        <allow_onsets> type -noonset to ban onset consonants
        <allow_repeats> type -noreps to ban repeat word generation
        ex:
                python wordgen.py 50 2 -nocluster
                python wordgen.py 23 3 -nodip
                python wordgen.py 16 1
                python wordgen.py 38 4 -nocluster -nodip