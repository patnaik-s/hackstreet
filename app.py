from flask import *
import os
from pprint import pprint
import nltk
nltk.download('stopwords')
from Questgen import main
from requests_html import HTMLSession

import spacy
from sense2vec import Sense2VecComponent,Sense2Vec                                         
from pathlib import Path
import openai

from dotenv import load_dotenv
load_dotenv()



"""Open AI"""
openai.api_key = os.getenv('API_OPENAI')
def WebSearcher(query):
    model_engine = "text-davinci-003"
    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=query,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )
    response = completion.choices[0].text
    return response

"""Function For Shortq"""
def shortQ(url):
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
    
    return output


app = Flask(__name__)



@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method=='POST':

        url=request.form.get('url')
        res=shortQ(url)['questions']
        for i in res:
            # webRes=WebSearcher(i['Question'])
            i["WebSearcher"]="API Limit Has been Reached"

        return render_template("index.html",result=res,start='okay')
    
    return render_template("index.html",result=None,start=None)


@app.route('/blog/<path:url>',methods=['POST','GET'])
def show(url):
    res=shortQ(url)['questions']
    for i in res:
        # webRes=WebSearcher(i['Question'])
        i["WebSearcher"]="API Limit Has been Reached"

    return render_template("index.html",result=res,start='okay')


@app.route('/api/<path:url>',methods=['POST','GET'])
def api(url):
    output =shortQ(url)['questions']
    for i in output:
        # webRes=WebSearcher(i['Question'])
        i["WebSearcher"]="API Limit Has been Reached"

    return jsonify(output)



app.run(debug=True)