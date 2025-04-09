'''
Python Script to build a corpus for a new Bible
Jonah Winchell
Code as a Liberal Art, Spring 2025
'''

'''
Original object stores key word, following words with number of occurences,
and total number of occurences of this word

temp = {
    'I': [
        {
            'am': 5,
            'will': 7,
            'do': 19
        },
        31
    ],
    'will': [
        {
            'not': 7,
            'never': 9
        },
        16
    ]
}

Final object stores key word and list of following words with their 
chance of occurence

markov_chain = {
    'I': {
        'am': .16,
        'will': .26,
        'do': .61
    },
    'will': {
        'not': .44,
        'never': .56
    }
}
'''

import re
import random


def main():
    cleaned_text = []
    # Open and clean the raw text
    with open('corpora/test.txt', 'r') as f:
        words = f.read().replace('\n', ' ').split()

        # Get rid of special characters
        pattern = re.compile(r'^[a-zA-Z]')
        for w in words:
            w = w.replace('"', '')
            w = w.replace('\'', '')
            if re.search(pattern, w):
                cleaned_text.append(w)
        
    markov = create_markov(cleaned_text)
    final_text = create_text(markov, 1000)
    print(final_text)
    return


''' Given a text, create a Markov Chain object and return it '''
def create_markov(text):
    markov_temp = {}
    markov_final = {}
    i = 0
    while i < len(text)-1:
        current = text[i]
        next = text[i+1]

        # If current word is already accounted for
        if current in list(markov_temp.keys()):
            # Add one to total occurences
            markov_temp[current][1] += 1
            possible_words = markov_temp[current][0]

            # If the next word is already accounted for, add an occurence
            if next in list(possible_words.keys()):
                possible_words[next] += 1
            # Else create entry for the next word and set occurences to 1
            else:
                possible_words[next] = 1
        # If current word not accounted for, add it
        else:
            markov_temp[current] = [
                { next: 1 }, 
                1
            ]

        i += 1
    
    # Create final entry for each word
    for w in list(markov_temp.keys()):
        possible_words = markov_temp[w][0]
        total_occurences = markov_temp[w][1]
        markov_final[w] = {}

        # Create list of possible next words and their likelihood to occur, 
        # rounded to nearest thousandth
        for n in list(possible_words.keys()):
            markov_final[w][n] = round(
                (possible_words[n] / total_occurences), 
                3)
    
    return markov_final


''' Given a Markov Chain object and length, return a generated text '''
def create_text(markov, length):
    text = ''
    i = 0
    # Choose a random word to start
    current_word = random.choice(list(markov.keys()))

    # Generate text
    while i < length-1:
        text += f'{current_word} '
        # List all possible next words
        possible_nexts = list(markov[current_word].keys())
        # List all weights associated with possible next words
        possible_nexts_weights = list(markov[current_word].values())
        # Choose a word according to weights
        next_word = random.choices(
            possible_nexts, 
            weights=possible_nexts_weights, 
            k=1)[0]
        current_word = next_word
        i += 1

    return text


if __name__ == '__main__':
    main()
