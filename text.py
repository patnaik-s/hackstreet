url = "https://www.searchenginejournal.com/google-ads-to-start-hiding-some-search-query-data/379840/" #@param {type:"string"}
selector = "p" #@param {type:"string"}
from requests_html import HTMLSession
session = HTMLSession()

with session.get(url) as r:

    paragraph = r.html.find(selector, first=False)

    text = " ".join([ p.text for p in paragraph])
print(text)