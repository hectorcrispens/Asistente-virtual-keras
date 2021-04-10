import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.tensorflow.org/guide/keras/train_and_evaluate'
res = requests.get(url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')
text = soup.find_all("p",text=True)

output = []
blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    # there may be more elements you don't want, such as "style", etc.
]

for t in text:
    output= output + t.text.split()

print(set(output))

df = pd.read_csv('corpus.csv', index_col=0)

#print(df)
