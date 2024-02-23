import pandas as pd
import argparse
from pathlib import Path

import newspaper
from newspaper.mthreading import fetch_news

output_path = Path('../article_text')
if not output_path.is_dir():
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
    args = parser.parse_args()
    return args

def get_articles_from_url(id_list: [str], url_list: [str], output_path: str) -> None:
    dataframe = {
        'id': [],
        'url': [],
        'publishedDate': [],
        'author': [],
        'text': [], 
    }
    results = fetch_news(url_list, threads=4)

    dataframe['id'] = id_list
    dataframe['url'] = [x.url for x in results]
    dataframe['publishedDate'] = [x.publish_date for x in results]
    dataframe['author'] = [x.authors for x in results]
    dataframe['text'] = [x.text for x in results]
    
    # article_list['source'] = article_source
    pd.DataFrame(dataframe).to_csv(article_input, index=False)

def main():
    args = _parse_arguments()
    
    # Get article ids from input file
    article_list = pd.read_csv(args.input_file)
    
    # Get input features
    id_list = article_list['id'].values
    url_list = article_list['url'].values
    
    # Get outputpath
    out_fn = os.path.join(output_path, args.output_file)
    
    # Call Dataframe creation function
    get_articles_from_url(id_list, url_list,out_fn)
