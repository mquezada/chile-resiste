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
    url = tweet.media_url
    tweet_id = tweet.tweet_id
    created_at = tweet.created_at

    resp = requests.get(url, allow_redirects=True)

    if resp.status_code == 200:
        folder = created_at.strftime('%Y%m%d')
        ts = created_at.strftime('%Y%m%d_%H%M%S')

        save_path = DATA_PATH / Path(folder)
        save_path.mkdir(exist_ok=True)

        fpath = save_path / Path(f'{ts}_{tweet_id}.mp4')

        with fpath.open('wb') as f:
            f.write(resp.content)
        set_downloaded(tweet.id, str(fpath))


tweets_no_downloaded = list(get_tweets())
#pool = multiprocessing.Pool(16)
#pool.imap_unordered(download, tweets_no_downloaded)

for t in tqdm(tweets_no_downloaded):
    download(t)
