#!/usr/bin/env python3
"""
Source: https://github.com/hsci-r/finnish-media-scrapers/blob/master/finnish_media_scrapers/scripts/query_hs.py
Command-line script for querying Helsingin Sanomat
"""


import argparse
import asyncio
import csv
import logging
import random
from datetime import datetime
from time import sleep
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

import aiohttp

from query import query_hs
from metadata_writer import write_metadata

load_dotenv(dotenv_path=find_dotenv())

output_path = os.environ.get('FINNISH_NEWSCRAPER_OUTPUT')
if not Path(output_path).is_dir():
    os.makedirs(output_path)

SOURCE = 'Helsingin Sanomat'
logging.basicConfig(level=logging.INFO)

def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from-date',
                        help="from date (inclusive, YYYY-MM-DD)", required=True)
    parser.add_argument('-t', '--to-date', help="to date (inclusive, YYYY-MM-DD, defaults to today)",
                        default=datetime.today().strftime('%Y-%m-%d'))
    parser.add_argument(
        '-q', '--query', help="query string to search for", required=True)
    parser.add_argument(
        '-o', '--output', help="output CSV file", required=True)
    parser.add_argument(
        '-l', '--limit', help="number of articles to fetch per query (50/100)", default=100, type=int)
    parser.add_argument(
        '-d', '--delay', help="number of seconds to wait between consecutive requests", default=1, type=int)
    parser.add_argument('--quiet', default=False,
                        action='store_true', help="Log only errors")
    return parser.parse_args()


async def _amain():
    args = _parse_arguments()

    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
        
    output_fn = os.path.join(output_path, args.output)

    with open(output_fn, "w", encoding="utf-8") as output_file:
        csv_output = csv.writer(output_file)
        csv_output.writerow(['id', 'source', 'url', 
                            #  'createdAt', 'updatedAt', 
                             'headline'])
        total_count = 0
        async with aiohttp.ClientSession() as session:
            async for response in query_hs(session, args.query, args.from_date, args.to_date, args.limit):
                total_count += len(response.articles)
                logging.info(
                    "Processing %d articles from %s. In total fetched %d articles.",
                    len(response.articles), response.url, total_count)
                for article in response.articles:
                    csv_output.writerow([article.id, 
                                         article.source,
                                         article.url,
                                         article.api_url,
                                        #  article.date_created,
                                        #  article.date_modified,
                                         article.title
                                        ])
                sleep(random.randrange(args.delay*2))
            logging.info("Processed %s articles in total.", total_count)
    
    write_metadata(response.url, SOURCE, args.query, total_count, args.output)

def main():
    asyncio.run(_amain())


if __name__ == '__main__':
    main()