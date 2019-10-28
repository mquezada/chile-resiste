import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime

#engine = create_engine('mysql+pymysql://mq:mq@localhost:3306/manifestaciones')
Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(BigInteger)
    user_id = Column(BigInteger)
    user_handle = Column(String)
    user_name = Column(String)
    verified = Column(Boolean)
    user_followers = Column(Integer)
    user_followees = Column(Integer)
    user_lang = Column(String)
    user_location = Column(String)
    user_statuses = Column(Integer)
    tweet_lang = Column(String)
    created_at = Column(DateTime)
    rts = Column(Integer)
    likes = Column(Integer)
    media_url = Column(String)
    media_type = Column(String)
    duration = Column(Integer)
    text = Column(String)
    downloaded = Column(Boolean)


class DownloadPath(Base):
    __tablename__ = 'download_path'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(BigInteger)
    download_path = Column(String)