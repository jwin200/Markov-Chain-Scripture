'''
Python Script to build a corpus for a more interesting Old Testament
Jonah Winchell
Code as a Liberal Art, Spring 2025
'''

import re
import os
import requests
from bs4 import BeautifulSoup as bs, SoupStrainer

tanakh_index = 'https://archive.org/download/kjv-text-files'
lotr_index = 'https://dn721603.ca.archive.org/0/items/tolkien-j.-the-lord-of-the-rings-harper-collins-ebooks-2010/Tolkien-J.-The-lord-of-the-rings-HarperCollins-ebooks-2010_djvu.txt'
hobbit_index = 'https://dn720001.ca.archive.org/0/items/hobbit_202201/hobbit_djvu.txt'


''' Scrape and download the Tanakh '''
def download_tanakh():
    tanakh_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 
                   'SongofSolomon', 'Joshua', 'Judges', 'Samuel', 'Kings', 
                   'Isaiah', 'Jeremiah', 'Ezekiel', 'Hosea', 'Joel', 'Amos',
                   'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
                   'Haggai', 'Zechariah', 'Malachi', 'Psalms', 'Proverbs', 'Job',
                   'Ruth', 'Lamentations', 'Ecclesiastes', 'Esther', 'Daniel',
                   'Ezra', 'Chronicles']

    response = requests.get(tanakh_index)
    soup = bs(response.content, 'html.parser', parse_only=SoupStrainer('tr'))
    soup.prettify()
    for link in soup.find_all('a'):
        if link.has_attr('href') and re.match(r'^[A-Z].*', link['href']):
            link_name = link['href'].split('.')[0]
            # Check if we already have this text
            if f'{link_name}.txt' in os.listdir('corpus'):
                print(f'{link_name} already downloaded...')
                continue
            # Download if we have a matching text name
            if link_name in tanakh_books:
                new_response = requests.get(f'{tanakh_index}/{link_name}.txt')
                text = str(bs(new_response.content, 'html.parser'))

                with open(f'corpus/{link_name}.txt', 'w') as f:
                    f.write(text)


''' Scrape and download The Lord of the Rings '''
def download_LOTR():
    if 'lotr.txt' in os.listdir('corpus'):
        print(f'Lord of the Rings already downloaded...')
        return

    include = False

    # Get text from website
    response = requests.get(lotr_index)
    text = str(bs(response.content, 'html.parser'))
    lines = list(iter(text.splitlines()))
    final_text = ''

    # Go through each line of text
    for l in lines:
        if include:
            # Stop when we hit the appendix
            if 'APPENDIX' in l:
                break
            # If the line contains valid text, include it
            elif re.match(r'^[a-zA-Z].*', l) and not re.match(r'.*[1-9].*', l):
                # Catch hyphenated line breaks
                if re.search(r"- ", l):
                    new_l = l[:-2]
                    final_text += new_l
                else:
                    final_text += f'{l}\n'
        # Once we hit the prologue, start including text
        elif 'accessory volume.' in l:
            include = True

    # Save text to local file
    with open(f'corpus/lotr.txt', 'w') as f:
        f.write(final_text)


''' Scrape and download The Hobbit '''
def download_hobbit():
    if 'hobbit.txt' in os.listdir('corpus'):
        print(f'The Hobbit already downloaded...')
        return

    include = False

    # Get text from website
    response = requests.get(hobbit_index)
    text = str(bs(response.content, 'html.parser'))
    lines = list(iter(text.splitlines()))
    final_text = ''

    # Go through each line of text
    for l in lines:
        if include:
            # If the line contains valid text, include it
            if re.match(r'^[a-zA-Z].*', l) and not re.match(r'.*[1-9].*', l):
                final_text += f'{l}\n'
        # Once we hit the first chapter, start including text
        elif 'An Unexpected Party' in l:
            include = True

    # Save text to local file
    with open(f'corpus/hobbit.txt', 'w') as f:
        f.write(final_text)


if __name__ == '__main__':
    download_tanakh()
    download_LOTR()
    download_hobbit()
