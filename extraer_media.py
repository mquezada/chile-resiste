import json
import sys
from tqdm import tqdm
import os
import re
import pandas as pd
import datetime


if len(sys.argv) < 3:
    print("usage: extraer_media.py <path-to-tweets.json> <path-to-output-file>")

filename = sys.argv[1]
output = sys.argv[2]

video_match = 'https://twitter.com/.*/status/[0-9]+/video/1'

colnames = [
    'tweet_id',
    'user_id',
    'user_handle',
    'user_name',
    'verified',
    'created_at',
    'rts',
    'likes',
    'media_url',
    'media_type',
    'duration',
    'text'
]


def process_lines(f):
    media_urls = set()

    results = []
    for line in tqdm(f, desc="processing file"):
        j = json.loads(line)

        if 'retweeted_status' in j:
            j = j['retweeted_status']

        tweet_id = j['id_str']
        user_id = j['user']['id_str']
        user_handle = j['user']['screen_name']
        user_name = j['user']['name']
        verified = int(j['user']['verified'])
        rts = j['retweet_count']
        likes = j['favorite_count']
        created_at = j['created_at']
        created_at = datetime.datetime.strptime(
            created_at, '%a %b %d %H:%M:%S %z %Y').strftime("%Y-%m-%d %H:%M:%S")

        text = ' '.join(j['full_text'].split())

        medias = []

        entities = j.get('entities')
        if entities:
            medias_ = entities.get('media')
            if medias_:
                for media in medias_:
                    media_type = media.get('type')
                    expanded_url = media.get('expanded_url')
                    if re.match(video_match, expanded_url):
                        media_type = 'thumbnail'
                    media_url = media.get('media_url')
                    duration = 'NA'
                    medias.append((media_url, media_type, duration))

        extended_entities = j.get('extended_entities')
        if extended_entities:
            medias_ = extended_entities.get('media')
            if medias_:
                for media in medias_:
                    media_type = media.get('type')
                    if media_type == 'video':
                        video_info = media.get('video_info')
                        if video_info:
                            variants = video_info.get('variants')
                            v = min([v for v in variants if v['content_type']
                                     == 'video/mp4'], key=lambda _v: _v['bitrate'])
                            media_url = v['url']
                            duration = video_info['duration_millis']
                            medias.append((media_url, media_type, duration))

        for media_url, media_type, duration in medias:
            if media_url in media_urls:
                continue
            if media_type != 'video':
                continue

            media_urls.add(media_url)
            results.append([tweet_id, user_id, user_handle, user_name, verified,
                            created_at, rts, likes, media_url, media_type, duration, f'"{text}"'])
    return results


with open(filename, 'r') as f:
    results = process_lines(f)

df = pd.DataFrame(results)
df.to_csv(output, sep=',', header=False, index=False)

#for tweet_id, user_id, user_handle, user_name, verified, created_at, rts, likes, media_url, media_type, duration, text in tqdm(results, desc="writing results"):
#    g.write(+ '\n')