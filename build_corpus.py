'''
Python Script to build a corpus for a new Bible
Jonah Winchell
Code as a Liberal Art, Spring 2025
'''

import json
import re
import requests
from bs4 import BeautifulSoup as bs

index = 'https://www.sefaria.org/Genesis.1.1?lang=en&aliyot=0'

response = requests.get(index)
# start = 'DJANGO_VARS'
# end = 'STRAPI_INSTANCE'
# m = re.compile(r'DJANGO_VARS(.*?)', re.MULTILINE)
# n = re.compile(r'(.*?)STRAPI_INSTANCE', re.MULTILINE)

# x = re.compile(r"^(.+?)(DJANGO_VARS).*\n((?:\n.+)+)", re.MULTILINE)
# x = re.compile(r'(DJANGO_VARS).*(STRAPI_INSTANCE)', re.DOTALL)
# print(re.search(x, response).string)
# exit()


start = re.search('DJANGO_VARS', response.text).span()[0]+14
end = re.search('STRAPI_INSTANCE', response.text).span()[0]-4
j = response.text[start:end]
clean = re.sub(r'\n|\r|\t', '', j)
#clean = re.sub(r'(?<!\")\:', '"props"', clean)
print(clean)
exit()
print(clean)
new = json.loads(clean)
print(new)
exit()


with open('corpora/c1.txt', 'r') as f:
    txt = f.read()
    
    
    #print(re.search(m, response))
    print(re.search('DJANGO_VARS', txt).span()[0])
    print(re.search('STRAPI_INSTANCE', txt).span()[0]-1)


soup = bs(response.content, features='html.parser')
soup.prettify()
print(response)
#exit()
# results = soup.find_all('tr', attrs={'class': 'Co_Verse'})
results = soup.find_all('tr')
print(results)

exit()

with open('corpora/c1.txt', 'w') as f:
    for r in results:
        f.write(str(r))

#print(soup)