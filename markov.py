'''
Python Script to spice up the Old Testament
Jonah Winchell
Code as a Liberal Art, Spring 2025
'''

import re
import os
import json
import random
import argparse


''' Parse command line arguments '''
def __parse():
    parser = argparse.ArgumentParser(description = 'Outline your next Scripture!',
                                    formatter_class = argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-v', '--verses',
                        metavar='V',
                        dest='verses',
                        default=30,
                        type=int,
                        help='Specify the number of verses you\'d like to generate, optional')
    
    parser.add_argument('-o', '--output',
                        metavar='O',
                        dest='output',
                        default='final.txt',
                        help='Optional name of desired output file, defaults to: "final.txt"')
    
    return vars(parser.parse_args())


def __main():
    args = __parse()
    markov = {}
    
    # If a Markov Chain exists, load it
    if os.path.exists('markov_chain.json'):
        with open('markov_chain.json', 'r') as f:
            print('Loading Markov Chain from JSON file')
            markov = json.load(f)
    # Else create a new one from our corpora
    else:
        print('Creating new Markov Chain from corpus')
        tokenized_text = []
        # Open and clean all texts in corpora folder
        for name in os.listdir('corpus'):
            if 'DS_Store' not in name:
                with open(f'corpus/{name}', 'r') as f:
                    # Get rid of special characters
                    words = f.read().replace('\n', ' ').split()
                    for w in words:
                        w = w.replace('"', '')
                        w = w.replace('\'', '')
                        # Stray apostrophes everywhere for some reason
                        if re.match(r'.*[’|\)]$', w):
                            w = w[:-1]
                        if re.search(r'^[a-zA-Z]', w) and re.match(r'.*[a-z].*', w):
                            tokenized_text.append(w)
        # Generate new Markov Chain
        markov = create_markov(tokenized_text)

        with open('markov_chain.json', 'w') as f:
            json.dump(markov, f)
    
    # Generate given number of verses
    final_text = create_text(markov, args['verses'])

    with open(f'output/{args['output']}', 'w') as f:
        f.write(final_text)
    return


''' Given a tokenized text, return a Markov Chain object '''
def create_markov(text):
    markov_temp = {}
    markov_final = {}
    total_length = len(text)
    i = 0

    # Go through the whole text
    while i < total_length-2:
        current = text[i]
        next = text[i+1]

        # If current word is already accounted for
        if current in list(markov_temp.keys()):
            # Add one to total occurences
            possible_words = markov_temp[current]
            # If the next word is already accounted for, add an occurence
            if next in list(possible_words.keys()):
                possible_words[next] += 1
            # If the next word is not accounted for, create an entry
            else:
                possible_words[next] = 1
        # If current word is not accounted for, create an entry
        else:
            markov_temp[current] = { next: 1 }
        
        i += 1
        # Loading screen
        __stats(total_length, i)
    
    # Create final object with all words and combos
    for w in list(markov_temp.keys()):
        possible_words = markov_temp[w]
        total_occurences = sum(list(markov_temp[w].values()))
        markov_final[w] = {}

        # Create dictionary of possible next words and their likelihood 
        # to occur, rounded to nearest hundred thousandth
        for n in list(possible_words.keys()):
            markov_final[w][n] = round(
                (possible_words[n] / total_occurences), 
                5)
    
    return markov_final


''' Given a Markov Chain object and length, return a generated text '''
def create_text(markov, length):
    verse = 1
    end_verse = True
    text = 'Book of '

    # Create title
    exclude = ['Israel', 'Egypt']
    options = list(markov['of'].keys())
    option_weights = list(markov['of'].values())
    while True:
        choice = random.choices(
                    options, 
                    weights=option_weights, 
                    k=1)[0]
        choice = ''.join(filter(str.isalpha, choice))   # Black magic

        # Must be a proper noun (exclude israel and egypt, too common)
        if re.match(r'^[A-Z].*', choice) and choice not in exclude:
            text += f'{choice}\n\n'
            break

    # Choose a random word to start
    current_word = random.choice(list(markov.keys()))
    uppercase = False

    # Generate text
    while verse <= length:
        chance = random.randrange(0, 3)
        # Capitalize new sentences
        word = current_word
        if uppercase:
            word = word.title()
            uppercase = False
        # If verse has ended, start a new one
        if end_verse:
            text += f'[{verse}] {word.title()} '
            end_verse = False
        # If a word ends with punctuation, possibly end this verse
        elif re.match(r'.*[^a-zA-Z]$', word) and chance == 0:
            text += f'{word}\n'
            end_verse = True
            verse += 1
        # Else, add a new word to the verse
        else:
            text += f'{word} '
        
        # List all possible next words
        possible_nexts = list(markov[current_word].keys())
        # List all weights associated with possible next words
        possible_nexts_weights = list(markov[current_word].values())
        # Choose a word according to weights
        next_word = random.choices(
            possible_nexts, 
            weights=possible_nexts_weights, 
            k=1)[0]
        # If sentence ended, next word uppercase
        if re.match(r'.*[\.|\!|\?]$', current_word):
            uppercase = True

        current_word = next_word

    return text


''' Display loading messages '''
def __stats(length, i):
    print(f'\tCreating Markov Chains                   \n'
          f'\t{round((i / length) * 100, 3)}% done     \n',
          end='\r\033[A\r\033[A')


if __name__ == '__main__':
    __main()
