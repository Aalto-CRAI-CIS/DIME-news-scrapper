import aiohttp
from aiohttp import ClientSession
import asyncio

import time
import logging
import json
import argparse
from pathlib import Path
import os
from datetime import datetime
import pandas as pd

articles_out_path = Path('../article_json')

if not articles_out_path.is_dir():
    os.makedirs(articles_out_path)
    
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
    parser.add_argument(
        '-s', '--source', 
        help="Chose between Iltalehti, Ilta-Sanomat, YLE News, Helsingin Sanomat", 
        required=True,
        choices=['Iltalehti', 'Ilta-Sanomat', 'YLE News', 'Helsingin Sanomat']
    )
    parser.add_argument('--quiet', default=False,
                    action='store_true', help="Log only errors")

    args = parser.parse_args()
    return args


async def fetch_articles(session: ClientSession, url: str):
    async with session.get(url) as response:
        if response.status != 200:
            raise ValueError(f"Got unexpected response code {response.status} for {response.url}.")
        response_json = (await response.json())['response']
        if response_json is None:
            raise ValueError(f"Got empty response for {response.url}")
        return response_json

async def _amain(article_ids:[str], article_api_url: [str], article_output_path: str) -> None:
    responses = {}
    async with aiohttp.ClientSession() as session:
        for i, _id in enumerate(article_ids):
            url = article_api_url[i]
            responses[_id] = await fetch_articles(session, url)
            time.sleep(6) # delay 6s after each request
            
    with open(article_output_path, "w") as write_file:
        json.dump(responses, write_file)            

def main():
    args = _parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    
    # Get article ids from input file
    df = pd.read_csv(args.input_file)
    ids = df['id'].values
    urls = df['apiURL'].values
    
    # Get output path
    article_output = os.path.join(articles_out_path, args.output_file)
    
    asyncio.run(_amain(ids, urls, article_output))

if __name__ == '__main__':
    main()