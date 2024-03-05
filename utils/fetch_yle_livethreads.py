import aiohttp
from aiohttp import ClientSession
import asyncio

import json
import os
import time 

import pandas as pd
from scripts.fetch import fetch_articles 

async def _amain(feed_ids:[str], article_output_path: str) -> None:
    responses = {}
    async with aiohttp.ClientSession() as session:
        for i, _id in enumerate(feed_ids):
            url = f'https://livefeed-data.api.yle.fi/v2/live/{_id}/updates'
            params = {
                'app_id': 'ukko',
                'createdBefore': '2024-03-05',
            }
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
                "Accept": "*/*",
                "Authorization": "y6gq9xO6ZHHCV0r097WV6aESQrdCWFu2",
                "Sec-Fetch-Mode": "cors",
                }
            responses[str(_id)] = await fetch_articles(session, url, params, headers)
            print(responses[str(_id)] )
            time.sleep(6) # delay 6s after each request
            if i % 100 == 1: # interval saving
                interval_saving_path = f'{os.path.splitext(article_output_path)[0]}_temp.json'
                with open(interval_saving_path, "w") as write_file:
                    json.dump(responses, write_file)  
        
    with open(article_output_path, "w") as write_file:
        json.dump(responses, write_file)

def fetch_livethreads(feed_ids:[str], article_output_path: str):
    asyncio.run(_amain(feed_ids, article_output_path))
