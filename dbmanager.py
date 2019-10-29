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


def get_tweets(downloaded=False, limit=30000):
    with session.begin():
        tweets = session.query(Tweet).filter_by(downloaded=downloaded).limit(limit)
        return tweets.all()

def set_downloaded(row_id, path):
    with session.begin():
        tweet = session.query(Tweet).filter_by(id=row_id).first()
        tweet.downloaded = True

        dpath = DownloadPath(tweet_id=tweet.tweet_id, download_path=path)
        session.add(dpath)

def set_downloaded_bulk(data):
    with session.begin():
        for row_id, path in data:
            tweet = session.query(Tweet).filter_by(id=row_id).first()
            tweet.downloaded = True

            dpath = DownloadPath(tweet_id=tweet.tweet_id, download_path=path)
            session.add(dpath)