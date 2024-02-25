#!bin/bash
### Get argument

# News agent target

# Query

# From date

# To date

# Limit

# Output file name

# Delay


echo "Get a list of articles meeting the query {} in news agent {} between {} and {}"

# If depending on target
# python3 scripts/query_il.py -f 2023-10-01 -t 2024-01-01 -q korona -o korona-il-aug-dec-2023.csv 
# python3 scripts/query_is.py -f 2023-10-01 -t 2024-01-01 -q korona -o korona-is-aug-dec-2023.csv 
# python3 scripts/query_yle.py -f 2023-10-01 -t 2024-01-01 -q korona -o korona-yle-aug-dec-2023.csv 

echo "Get a list of json responses when querying article API"

# python3 scripts/fetch.py -i korona-il-aug-dec-2023.csv -o korona-il-aug-dec-2023.json
# python3 scripts/fetch.py -i korona-is-aug-dec-2023.csv -o korona-is-aug-dec-2023.json
# python3 scripts/fetch.py -i korona-yle-aug-dec-2023.csv -o korona-yle-aug-dec-2023.json

echo "Get the formatted text for each article"
# python3 scripts/newspaper4k_scrapper.py -i korona-il-aug-dec-2023.csv -o korona-il-aug-dec-2023.csv

# python3 scripts/article_parser.py -i korona-il-aug-dec-2023.json -o korona-il-aug-dec-2023.csv -s Iltalehti
# python3 scripts/article_parser.py -i korona-is-aug-dec-2023.json -o korona-is-aug-dec-2023.csv -s Ilta-Sanomat
# python3 scripts/article_parser.py -i korona-yle-aug-dec-2023.json -o korona-yle-aug-dec-2023.csv -s 'YLE News'


echo "Generate output file"
# python3 scripts/merge.py -i korona-il-aug-dec-2023.csv -o korona-il-aug-dec-2023.csv
# python3 scripts/merge.py -i korona-is-aug-dec-2023.csv -o korona-is-aug-dec-2023.csv
# python3 scripts/merge.py -i korona-yle-aug-dec-2023.csv -o korona-yle-aug-dec-2023.csv