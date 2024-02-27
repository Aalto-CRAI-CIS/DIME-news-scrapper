"""
This script merge results from 3 seperate web-scrapping module into 1 big dataframe with structure described as in README

"""

from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import logging
import json
import argparse
import os
from datetime import datetime, timedelta

import pandas as pd

load_dotenv(dotenv_path=find_dotenv())

# Make output dir if not exist
output_path = os.environ.get('MERGED_OUTPUT')
if not Path(output_path).is_dir():
    os.makedirs(output_path)

# Read input and output filename 
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

def get_date_info(source, article_data):
    """Find relevant fields from API responses to get original published date and updated date data"""
    if source == 'Iltalehti':
        return {
            'createdAt': article_data['published_at'],
            'updatedAt': article_data['updated_at']
        }
    if source == 'Ilta-Sanomat' or source == 'Helsingin Sanomat':
            if 'assetData' in article_data.keys():
                return {    
                    # TODO: ## Find out what is the different between publishedDate, and these
                    'createdAt': article_data['assetData']['sharingMetadata']['startDate'], 
                    'updatedAt': article_data['assetData']['sharingMetadata']['modifiedDate']
                }
            else:
                print(f"NOTE: Article keys are: {article_data.keys()}")
                return {    
                    # TODO: ## Find out what is the different between publishedDate, and these
                    'createdAt': '', 
                    'updatedAt': ''
                }
    if source == 'YLE News':
        return {
            # TODO: Get the correct attributes
            'createdAt': article_data['data'][0]['datePublished'],
            'updatedAt': article_data['data'][0]['dateContentModified']
        }
    pass

# Read Finnish new_scrapper dataframe:
def article_list(input_file: str) -> pd.DataFrame | None:
    article_list_path = os.path.join(os.environ.get('FINNISH_NEWSCRAPER_OUTPUT'), input_file)
    try:
        articles_df = pd.read_csv(article_list_path)
        return articles_df
    except Exception as e:
        print(f"Error when trying to read article list: {e}")
        raise ValueError(f"Got unexpected path {article_list_path}.")

# Read article json response data into a dataframe:
def article_json(input_file: str, source: str) -> pd.DataFrame | None:
    
    date_data_dict = {
        'id': [],
        'createdAt': [],
        'updatedAt': []
    }
    article_json_path = os.path.join(os.environ.get('ARTICLE_API_OUTPUT'), input_file)
    try:
        with open(article_json_path) as user_file:
            parsed_json = json.load(user_file)
            
        for (article_id, article_data) in parsed_json.items():
            dates = get_date_info(source, article_data)
            date_data_dict['id'].append(article_id)
            date_data_dict['createdAt'].append(dates['createdAt'])
            date_data_dict['updatedAt'].append(dates['updatedAt'])
        return pd.DataFrame(date_data_dict)
    
    except Exception as e:
        print(f"Error when trying to read article json response from API: {e}")
        raise e

# Read article text into a dataframe:
def article_text(input_file: str) -> pd.DataFrame | None:
    article_list_path = os.path.join(os.environ.get('NEWSPAPER4K_OUTPUT'), input_file)
    try:
        articles_text_df = pd.read_csv(article_list_path)
        return articles_text_df
    except Exception as e:
        print(f"Error when trying to read article list: {e}")
        raise ValueError(f"Got unexpected path {article_list_path}.")


def main():
    args = _parse_arguments()
    
    # Get article list
    article_list_df = article_list(args.input_file)
    
    # Get source
    source = article_list_df['source'][0] 
    
    # Get article dates df
    article_dates_df = article_json(args.input_file.split('.')[:-1][0]+'.json', source)

    # Get article text df
    article_text_df = article_text(args.input_file)
    
    # id_process:
    article_list_df['id'] = article_list_df['id'].apply(lambda x: str(x).rstrip().lstrip())
    article_dates_df['id'] = article_dates_df['id'].apply(lambda x: str(x).rstrip().lstrip())
    article_text_df['id'] = article_text_df['id'].apply(lambda x: str(x).rstrip().lstrip())
    
    # Merge output
    df = article_list_df.merge(article_dates_df, on=['id'], how='inner')
    df = df.merge(article_text_df, on=['id'],  how='inner')
    
    # Get outputpath
    out_fn = os.path.join(output_path, args.output_file)
    df.to_csv(out_fn, index=False)

if __name__ == '__main__':
    main()