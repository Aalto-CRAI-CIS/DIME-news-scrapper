import aiohttp
from aiohttp import ClientSession
import asyncio

import json
import os
import time 
import sys

import logging
logging.basicConfig(level=logging.INFO)

from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).parent.parent.parent))
logging.info(sys.path)
from scripts.fetch import fetch_articles 

async def _amain(feed_ids:[str], article_output_path: str) -> None:
    responses = {}
    async with aiohttp.ClientSession() as session:
        for i, _id in enumerate(feed_ids):
            _ids = _id.split('-')
            _ids[1] = '2'
            _id_new = '-'.join(_ids)
            url = f'https://livefeed-data.api.yle.fi//v2/feed/{_id_new}/post'
            params = {
                'app_id': 'ukko',
                'createdBefore': '2024-02-27T04:02:54.010Z',
                'limit': 5000
            }
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
                "Accept": "*/*",
                "Authorization": "y6gq9xO6ZHHCV0r097WV6aESQrdCWFu2",
                "Sec-Fetch-Mode": "cors",
                }
            try:
                responses[str(_id_new)] = await fetch_articles(session, url, params, headers)
                logging.info('SUCCESS when requesting live threads with url: %s', url)
            except Exception as e:
                logging.info('Got an error when requesting live threads with url: %s', url)
                url = f'https://livefeed-data.api.yle.fi/v2/live/{_id}/updates'
                responses[str(_id)] = await fetch_articles(session, url, params, headers)
            time.sleep(6) # delay 6s after each request
            if i % 2 == 1: # interval saving
                interval_saving_path = f'{os.path.splitext(article_output_path)[0]}_temp.json'
                with open(interval_saving_path, "w") as write_file:
                    json.dump(responses, write_file)  
        
    with open(article_output_path, "w") as write_file:
        json.dump(responses, write_file)

def fetch_livethreads(feed_ids:[str], article_output_path: str):
    asyncio.run(_amain(feed_ids, article_output_path))

if __name__ == '__main__':
    # TODO: make this generic
    feed_ids = ['64-1-16',
                 '64-1-2070',
                 '64-1-1044',
                 '64-1-2237',
                 '64-1-832',
                 '64-1-1080',
                 '64-1-2141',
                 '64-1-449',
                 '64-1-1177',
                 '64-1-1432',
                 '64-1-7',
                 '64-1-164',
                 '64-1-1438']
    output_path = 'livethread_json'
    if not Path(output_path).is_dir():
        os.makedirs(output_path)
    article_output_path = os.path.join(output_path, 'yle_livethreads.json')
    fetch_livethreads(feed_ids, article_output_path)