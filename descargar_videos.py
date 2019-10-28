import sqlalchemy 
import pandas as pd 
import requests
from sqlalchemy import create_engine
import multiprocessing
import datetime
from dbmanager import *
from pathlib import Path
from tqdm import tqdm

DATA_PATH = Path('/mnt/volume_nyc1_02/videos_save')

def download(tweet):
    id = tweet[0]
    url = tweet[1]
    tweet_id = tweet[2]
    created_at = tweet[3]

    resp = requests.get(url, allow_redirects=True)

    if resp.status_code == 200:
        folder = created_at.strftime('%Y%m%d')
        ts = created_at.strftime('%Y%m%d_%H%M%S')

        save_path = DATA_PATH / Path(folder)
        save_path.mkdir(exist_ok=True)

        fpath = save_path / Path(f'{ts}_{tweet_id}.mp4')

        with fpath.open('wb') as f:
            f.write(resp.content)
        
        return id, str(fpath)


tweets_no_downloaded = get_tweets()
data = [(t.id, t.media_url, t.tweet_id, t.created_at) for t in tweets_no_downloaded]

pool = multiprocessing.Pool(16)
for res in pool.imap_unordered(download, data):
    set_downloaded(res[0], res[1])

#for t in tqdm(tweets_no_downloaded):
#    download(t)
