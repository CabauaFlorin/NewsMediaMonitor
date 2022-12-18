from flask import Flask, request
import os
from newsapi import NewsApiClient
import newsapi
import spacy
from datasets import load_dataset
import json
from spacy.matcher import Matcher

ronec = load_dataset("ronec")
nlp = spacy.load("ro_core_news_lg")

app = Flask("NewsApp")

def getNewsContent(args):
    newsapi = NewsApiClient(api_key = os.environ.get("API_KEY"))
    data = newsapi.get_everything(q=args.get("title"), from_param=args.get("fromData"), to=args.get("toData"), sort_by=args.get("sort_by"), language=args.get("language")) #se mai poate adauga language='en' sau/si from_param='2019-06-15'
    results = data['articles'].copy()
    return list(results)

@app.get('/news')
def list_news():
    args = request.args;
    return getNewsContent(args)

@app.get('/nlp')
def get_nlp():
    args = request.args
    news = getNewsContent(args)
    x=[]
    for news_item in news:
        doc = nlp(news_item['content'])
        content_nlp=""
        for ent in doc.ents:
            content_nlp += ent.text + " | " + ent.lemma_ + " | " + ent.as_doc()[0].pos_ + " | " + ent.label_ + " | " + str(spacy.explain(ent.label_)) +"; "
            
        x.append({
            'title': news_item['title'],
            'url': news_item['url'],
            'content_nlp': content_nlp
        })
    return x

@app.get('/nlpDetailed')
def searchDetailed():
    args = request.args
    news = getNewsContent(args)

    detailed = []

    pattern = [{'LOWER': args},
              {'POS':'ADP','OP':'?'},
              {'POS':'PROPN'}]

    for news_item in news:
        doc = nlp(news_item['content'])

        matcher = Matcher(nlp.vocab)
        matcher.add(detailed, None, pattern)

        matches = matcher(doc)
        print(matcher)
        
        
    return pattern
        # for i in range(0, len(matches)):
        #     token = doc[matches[i][1]:matches[i][2]]
        #     detailed.append(str(token))

        # for detail in detailed:
        #     if (detail.split()[2] == ''):
        #         detailed.remove()

    
