from flask import Flask, request, render_template
import requests
from newspaper import Article
import sys
from urllib.parse import urlencode
import re
import os

app = Flask(__name__)


def scrape_url(url):
    article = Article(url)
    article.download()
    article.parse()
    article_text = article.text
    """
    if len(article_text)>1000:
        article_text = article_text[:1000]
    """
    print(len(article_text))
    sys.stdout.flush()
    return article_text


def text_preprocessing(raw_corpus):
    raw_corpus = raw_corpus.replace('\n', '')
    raw_corpus = re.split('[.?!]', raw_corpus)
    sentence_list = []
    for sentence in raw_corpus:
        if len(sentence)<=128:
            sentence_list.append(sentence)
        else:
            sentence_list.append(sentence[:128])
    return sentence_list


def analyze_binary(input_sentences):
    res = requests.post("https://hate-speech-binary-c2eedpqzcq-an.a.run.app/predict", json = {"input_sentences": input_sentences})
    if res.status_code != 200:
        raise Exception("Error: API request unsuccessful.")
    data = res.json()
    return data['predictions']


def analyze_topic(input_sentences):
    res = requests.post("https://hate-speech-topic-c2eedpqzcq-an.a.run.app/predict", json = {"input_sentences": input_sentences})
    if res.status_code != 200:
        raise Exception("Error: API request unsuccessful.")
    data = res.json()
    return data['predictions']


def analyze(input_sentences):
    binary_pred = analyze_binary(input_sentences)
    topic_input_sentences = [pred['sentence'] for pred in binary_pred if pred['label']=='혐오']
    data = analyze_topic(topic_input_sentences)
    return data


@app.route("/")
def index():
    requests.post("https://hate-speech-binary-c2eedpqzcq-an.a.run.app/wake", json = {"wake": 'wake'})
    requests.post("https://hate-speech-topic-c2eedpqzcq-an.a.run.app/wake", json = {"wake": 'wake'})
    return render_template("index.html")


@app.route("/scrape_page")
def scrape_page():
    return render_template("scrape_page.html")


@app.route("/input_page")
def input_page():
    return render_template("input_page.html")


@app.route("/loading")
def loading():
    input_sentences = request.args.to_dict()['input_sentences']
    input_sentences = input_sentences.strip('][').replace('\' ','').replace('\'','').split(', ')
    print(str(input_sentences))
    sys.stdout.flush()
    sentence_pairs = analyze(input_sentences)
    if len(sentence_pairs)==0:
        activation=False
    else:
        activation=True
    return render_template("results.html", sentence_pairs=sentence_pairs, activation=activation)


@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.form.get("url")
    article_text = scrape_url(url)
    input_sentences = text_preprocessing(article_text)
    input_sentences = {'input_sentences': input_sentences}
    input_sentences = urlencode(input_sentences)
    return render_template("loading.html", input_sentences=input_sentences)


@app.route("/input", methods=["POST"])
def input():
    input_text = request.form.get("input_text")
    input_sentences = text_preprocessing(input_text)
    input_sentences = {'input_sentences': input_sentences}
    input_sentences = urlencode(input_sentences)
    return render_template("loading.html", input_sentences=input_sentences)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
