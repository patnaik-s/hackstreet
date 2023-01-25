from pprint import pprint
import nltk
nltk.download('stopwords')
from Questgen import main
from requests_html import HTMLSession
session = HTMLSession()
url = "https://www.bajajfinservhealth.in/articles/sugarcane-juice-benefits" #@param {type:"string"}
selector = "p" #@param {type:"string"}
with session.get(url) as r:

    paragraph = r.html.find(selector, first=False)

    text = " ".join([ p.text for p in paragraph])
#print(text)

qe= main.QGen()
payload = {
            "input_text":text
        }
output = qe.predict_shortq(payload)
pprint (output)