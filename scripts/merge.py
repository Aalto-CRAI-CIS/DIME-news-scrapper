"""
This script merge results from 3 seperate web-scrapping module into 1 big dataframe with structure described as in README

"""

from pathlib import Path
import logging
import json
import argparse

import pandas as pd

# Make output dir if not exist
output_path = '/output'
if not articles_out_path.is_dir():
    os.makedirs(articles_out_path)

# Read 
