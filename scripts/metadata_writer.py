import csv
from datetime import datetime 
import uuid
from pathlib import Path
import os

metadata_path = Path('../meta-data')

if not metadata_path.is_dir():
    os.makedirs(metadata_path)
    
def write_metadata(url: str, source: str, query: str, n_articles: int, output_name: str) -> None:
    """Create and write meta-data of each scrape to `meta-data` directory using schema described in `README`"""
    # make a UUID from a string of hex digits (braces and hyphens ignored)
    scrape_id = str(uuid.uuid1())
    timestamp = str(datetime.now().isoformat())
    metadata_output = f'{output_name.split(".")[0]}-meta.csv'
    metadata_output = os.path.join(metadata_path, metadata_output)
    with open(metadata_output, "w", encoding="utf-8") as output_file:
        csv_output = csv.writer(output_file)
        csv_output.writerow(['scrape_id', 'date', 'url', 'source', 'query', 'n_articles'])
        csv_output.writerow([scrape_id, timestamp, url, source, query, n_articles])
        