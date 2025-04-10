'''
Python Script to build a corpus for a more interesting Old Testament
Jonah Winchell
Code as a Liberal Art, Spring 2025
'''

import re
import requests
from bs4 import BeautifulSoup as bs, SoupStrainer

index = 'https://archive.org/download/kjv-text-files'
index2 = 'https://dn721603.ca.archive.org/0/items/tolkien-j.-the-lord-of-the-rings-harper-collins-ebooks-2010/Tolkien-J.-The-lord-of-the-rings-HarperCollins-ebooks-2010_djvu.txt'


''' Scrape and download the Torah '''
def download_torah():
    torah_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']

    response = requests.get(index)
    soup = bs(response.content, 'html.parser', parse_only=SoupStrainer('tr'))
    soup.prettify()
    for link in soup.find_all('a'):
        if link.has_attr('href') and re.match(r'^[A-Z].*', link['href']):
            link_name = link['href'].split('.')[0]
            if link_name in torah_books:
                new_response = requests.get(f'{index}/{link_name}.txt')
                text = str(bs(new_response.content, 'html.parser'))

                with open(f'corpus/{link_name}.txt', 'w') as f:
                    f.write(text)


''' Scrape and download the Lord of the Rings '''
def download_LOTR():
    # Warning, absolutely terrible methods to clean the text lie below
    include = False

    # Get text from website
    response = requests.get(index2)
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
                final_text += f'{l}\n'
        # Once we hit the prologue, start including text
        elif 'accessory volume.' in l:
            include = True

    # Save text to local file
    with open(f'corpus/lotr.txt', 'w') as f:
        f.write(final_text)


if __name__ == '__main__':
    download_torah()
    download_LOTR()
