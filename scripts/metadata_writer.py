import csv
from datetime import datetime 
import uuid
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())
print(f'find_dotenv(): {find_dotenv()}')
output_path = os.environ.get('METADATA_OUTPUT')
print(f'output_path: {output_path}')
print()
if not Path(output_path).is_dir():
    os.makedirs(output_path)
   
# TODO: run this after merge  
def write_metadata(url: str, source: str, query: str, n_articles: int, output_name: str) -> None:
    """Create and write meta-data of each scrape to `meta-data` directory using schema described in `README`"""
    # make a UUID from a string of hex digits (braces and hyphens ignored)
    scrape_id = str(uuid.uuid1())
    timestamp = str(datetime.now().isoformat())
    metadata_output = os.path.join(output_path, output_name)
    with open(metadata_output, "w", encoding="utf-8") as output_file:
        csv_output = csv.writer(output_file)
        csv_output.writerow(['scrape_id', 'date', 'url', 'source', 'query', 'n_articles'])
        csv_output.writerow([scrape_id, timestamp, url, source, query, n_articles])
        