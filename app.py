from flask import Flask, request
import os
from newsapi import NewsApiClient
import newsapi
import spacy
from datasets import load_dataset
import json
from spacy.matcher import Matcher
import re

ronec = load_dataset("ronec")
nlp = spacy.load("ro_core_news_md")

app = Flask("NewsApp")

def getNewsContent(args):
    newsapi = NewsApiClient(api_key='ba79436deb7540b195686c7e9e046a72')
    data = newsapi.get_everything(q=args.get("title"), from_param=args.get("fromData"), to=args.get("toData"), sort_by=args.get("sort_by"), language=args.get("language")) #se mai poate adauga language='en' sau/si from_param='2019-06-15'
    results = data['articles'].copy()
    return list(results)

def split_sentences(text):
    text_splited = re.split('(\. )+|\n|\r\n', text)
    clean_sent = []
    for sentence in text_splited:
        if (sentence != ". "):
            clean_sent.append(sentence)
    return clean_sent

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

    sentences = []
    findedArgs = []

    for news_item in news:
        doc = nlp(news_item['content'])
        sentences.append(split_sentences(doc.text))

    pattern = [{'LOWER':args},
                {'POS':'ADP', 'OP':'?'},
                {'POS':'PROPN'}]

    matcher = Matcher(nlp.vocab)
    matcher.add("findedArgs", None, pattern)

    

    # for sentence in sentences:
    #     for item in sentence:

       
    #print(sentences[0][0])

    return pattern
