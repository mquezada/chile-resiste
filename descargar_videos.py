import sqlalchemy 
import pandas as pd 
import requests
from sqlalchemy import create_engine
import multiprocessing
import datetime

cnx = create_engine('mysql+pymysql://mq:mq@localhost:3306/manifestaciones')

df = pd.read_sql_query("SELECT * FROM tweets where downloaded=0", cnx)

def download(tweet_id, url):
    resp = requests.get(url, allow_redirects=True)
    if resp.status_code == 200:
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'/mnt/volume_nyc1_02/videos/{tweet_id}_{now}.mp4', 'wb') as f:
            f.write(resp.content)

data = list(map(tuple, list(df[['tweet_id', 'media_url']].values)))
pool = multiprocessing.Pool(16)
pool.starmap(download, data)