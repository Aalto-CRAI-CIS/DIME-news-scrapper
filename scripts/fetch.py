import aiohttp
from aiohttp import ClientSession
import asyncio

import time
from datetime import datetime
import logging
import json
import argparse
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

import pandas as pd

load_dotenv(dotenv_path=find_dotenv())

input_path = os.environ.get('FINNISH_NEWSCRAPER_OUTPUT')
output_path = os.environ.get('ARTICLE_API_OUTPUT')
if not Path(output_path).is_dir():
    os.makedirs(output_path)

    
def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-file', 
        help="Specify which input file to be used for fetching article ids", 
        required=True,
        )
    parser.add_argument(
        '-o', '--output-file', 
        help="Specify which output to save article jsons", 
        default=datetime.today().strftime('%Y-%m-%d')+"_article_jsons.json"
    )
    parser.add_argument('--quiet', default=False,
                    action='store_true', help="Log only errors")

    args = parser.parse_args()
    return args


async def fetch_articles(session: ClientSession, url: str, params=None, headers= None):
    async with session.get(url, params=params, headers=headers) as response:
        if response.status != 200:
            raise ValueError(f"Got unexpected response code {response.status} for {response.url}.")
        response_json = await response.json()
        
        if response_json is None:
            raise ValueError(f"Got empty response for {response.url}")
        
        return response_json['response'] if 'response' in response_json.keys() else response_json
    
async def _amain(article_ids:[str], article_api_url: [str], article_output_path: str) -> None:
    responses = {}
    async with aiohttp.ClientSession() as session:
        for i, _id in enumerate(article_ids):
            url = article_api_url[i]
            if 'https://articles.api.yle.fi//v2/articles.json' == url:
                params = {
                    'app_id': os.environ.get('YLE_APP_ID'),
                    'app_key': os.environ.get('YLE_APP_KEY'),
                    'id': _id
                }
                responses[str(_id)] = await fetch_articles(session, url, params)
            else:
                responses[str(_id)] = await fetch_articles(session, url)
            time.sleep(6) # delay 6s after each request
            if i % 100 == 1: # interval saving
                interval_saving_path = f'{os.path.splitext(article_output_path)[0]}_temp.json'
                with open(interval_saving_path, "w") as write_file:
                    json.dump(responses, write_file)  
        
    with open(article_output_path, "w") as write_file:
        json.dump(responses, write_file)  


def main():
    args = _parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    
    # Get article ids from input file
    if input_path in args.input_file:
        df = pd.read_csv(args.input_file)
    else: 
        df = pd.read_csv(os.path.join(input_path, args.input_file))
    
    # Get input features
    ids = df['id'].values
    urls = df['apiURL'].values
    
    # Get output path
    article_output = os.path.join(output_path, args.output_file)
    
    asyncio.run(_amain(ids, urls, article_output))

if __name__ == '__main__':
    main()