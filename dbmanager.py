from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from models import Tweet, DownloadPath

import logging

engine = create_engine('mysql+pymysql://mq:mq@localhost:3306/manifestaciones')
session_pool = sessionmaker(engine, autocommit=True)
session = session_pool()

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_tweets(downloaded=False):
    with session.begin():
        tweets = session.query(Tweet).filter_by(downloaded=downloaded)
        return tweets.all()

def set_downloaded(row_id, path):
    with session.begin():
        tweet = session.query(Tweet).filter_by(id=row_id).first()
        tweet.downloaded = True

        dpath = DownloadPath(tweet_id=tweet.tweet_id, path=path)
        session.add(dpath)
