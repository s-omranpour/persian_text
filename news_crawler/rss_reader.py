import requests
import re
from tqdm import tqdm
import feedparser
import json

sess = requests.Session()
home = 'https://www.tabnak.ir/fa/rss'
res = sess.get(home)

urls = []
for u in re.finditer('https://tabnak.ir/fa/rss/', res.text):
    s = u.start()
    e = res.text[s:].find('<')
    url = res.text[s:s+e]
    urls += [url]

def get_phrase(feed):
    phrases = []
    links = []
    for ent in feed['entries']:
        links += [ent['link']]
        phrases += [ent['title']]
        if 'summary' in ent.keys():
            phrases += [ent['summary']]
    return phrases, links

all_phrases = set()
all_links = set()
for url in tqdm(urls):
    res = sess.get(url)
    feed = feedparser.parse(res.text)
    ps, ls = get_phrase(feed)
    all_phrases.update(ps)
    all_links.update(ls)

json.dump(list(all_links), open('tabnak_urls.json','w'))
json.dump(list(all_phrases), open('tabnak_phrases.json','w'))