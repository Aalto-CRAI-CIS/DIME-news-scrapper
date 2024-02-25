from datetime import datetime, timedelta
import argparse
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os
import json

import pandas as pd

from article_parser_utils import Author, ArticleText
from parser_il import parser_il
from parser_is import parser_is
from parser_yle import parser_yle

load_dotenv(dotenv_path=find_dotenv())

input_path = os.environ.get('ARTICLE_API_OUTPUT')
output_path = os.environ.get('NEWSPAPER4K_OUTPUT')
if not Path(output_path).is_dir():
    os.makedirs(output_path)

def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--source', 
        choices=['Iltalehti', 'Ilta-Sanomat', 'Helsingin Sanomat', 'YLE News'],
        help="Specify which newspaper to parse article texts and authors", 
        required=True,
        )
    
    parser.add_argument(
        '-i', '--input-file', 
        help="Specify which input josn file to be used for fetching article ids", 
        required=True,
        )

    parser.add_argument(
        '-o', '--output-file', 
        help="Specify which output to save article jsons", 
        default=datetime.today().strftime('%Y-%m-%d')+"_article_jsons.json"
    )
    args = parser.parse_args()
    return args

def get_articles_from_url(art_text: [ArticleText], art_authors: [Author], output_path: str) -> None:
    dataframe = {}

    dataframe['id'] = [art.id_str for art in art_text]
    dataframe['author'] = [a for a in art_authors]
    dataframe['text'] = [art.text for art in art_text]
    pd.DataFrame(dataframe).to_csv(output_path, index=False)

def main():
    args = _parse_arguments()
    
    # Get article ids from input file
    input_fn = os.path.join(input_path, args.input_file)
    with open (input_fn, 'r') as json_f:
        json_obj = json.load(json_f)
    print(f'args.source: {args.source} and {args.source == "Iltalehti"}')
    
    if args.source == "Iltalehti":
        art_text, art_authors = parser_il(json_obj)
    if args.source == 'Ilta-Sanomat' or  args.source == 'Helsingin Sanomat':
        art_text, art_authors = parser_is(json_obj)
    if args.source == 'YLE News':
        art_text, art_authors = parser_yle(json_obj)
    # else:
    #     raise ValueError(f"{args.source} is must be in Iltalehti, Ilta-Sanomat, Helsingin Sanomat, or YLE News")
    
    # Get outputpath
    out_fn = os.path.join(output_path, args.output_file)
    print(f'out_fn {out_fn}')
    
    # Call Dataframe creation function
    get_articles_from_url(art_text, art_authors,out_fn)

if __name__ == '__main__':
    main()