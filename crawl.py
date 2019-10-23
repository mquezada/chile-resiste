import tweepy
from credenciales import *
from keywords import track
import content

import imp
imp.reload(content)

from content import vect, nlp

import datetime
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
import requests
import logging
import re
import spacy


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def resolve_url(url):
    res = requests.head(url, allow_redirects=True)
    return res.url

current_tweets = dict()
tweets = dict()

def cluster():
    global current_tweets
    global tweets 
    logging.info("cluster")
    ids, vectors = list(current_tweets.keys()), list(current_tweets.values())

    for i, v in enumerate(vectors):
        if len(v) == 0:
            del vectors[i]
            del ids[i]

    km = KMeans(n_clusters=3, n_init=100, n_jobs=-1)
    km.fit(vectors)
    clusters = km.labels_
    knn = NearestNeighbors(n_neighbors=1, n_jobs=-1)
    knn.fit(vectors)

    closests = knn.kneighbors(km.cluster_centers_)
    for idx in closests[1]:
        logging.info(f'https://twitter.com/waxkun/status/{tweets[ids[idx[0]]].id}')
        logging.info((idx, tweets[ids[idx[0]]].id, tweets[ids[idx[0]]].text))
        try:
            tweets[ids[idx[0]]].retweet()
            logging.info("retweeted")
        except Exception as e:
            logging.info(e)
        logging.info("")
    current_tweets = dict()
    tweets = dict()


def process_tweet(status):
    global current_tweets
    global tweets
    tweets[status.id] = status
    if hasattr(status, 'retweeted_status'):
        text = status.retweeted_status.text
    else:
        text = status.text
    vec, urls = vect(text, nlp)
    current_tweets[status.id] = vec
    #logging.info(text)


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.init = datetime.datetime.now()

    def on_status(self, status):
        process_tweet(status)
        now = datetime.datetime.now()
        if now - self.init > datetime.timedelta(minutes=1):
            cluster()
            self.init = now

myStreamListener = MyStreamListener(api)
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=track, languages=['es'])