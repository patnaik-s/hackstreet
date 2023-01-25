from flask import *

from pprint import pprint
import nltk
nltk.download('stopwords')
from Questgen import main
from requests_html import HTMLSession

import spacy
from sense2vec import Sense2VecComponent,Sense2Vec                                         
from pathlib import Path

app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        url=request.form.get('url')
        session = HTMLSession()
        selector = "p" 
        with session.get(url) as r:
            paragraph = r.html.find(selector, first=False)
        text = " ".join([ p.text for p in paragraph])

        qe= main.QGen()
        payload = {
                "input_text":text
            }
        output = qe.predict_shortq(payload)

        res=output['questions']
        return render_template("index.html",result=res,start='okay')
    
    return render_template("index.html",result=None,start=None)
@app.route('/blog/<path:s>',methods=['POST','GET'])
def show(s):
    session = HTMLSession()
    selector = "p" 
    with session.get(s) as r:
        paragraph = r.html.find(selector, first=False)
        text = " ".join([ p.text for p in paragraph])

        qe= main.QGen()
        payload = {
                "input_text":text
                }
        output = qe.predict_shortq(payload)

    res=output['questions']
    return render_template("index.html",result=res,start='okay')

app.run(debug=True,host='0.0.0.0')