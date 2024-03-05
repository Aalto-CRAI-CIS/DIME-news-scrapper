#!/bin/bash
####################################################################
# Get arguments
####################################################################
helpFunction()
{
   echo ""
   echo "Usage: $0 --source newsAgent --query searchWord  --from-date fromDate  --to-date toDate  --limit limit  --output-file csvFile"
   echo ""
   echo -e "\t  -s | --source newsAgent must be given. Current options are Iltalehti, Ilta-Sanomat, Helsingin Sanomat, YLE News"
   echo -e "\t  -q | --query searchWord is the topic of quiery. e.g., corona, 'gaza sota'"
   echo -e "\t  -f | --from-date fromDate is the starting date of search. Must given in YYYY-MM-DD format"
   echo -e "\t  -t | --to-date toDate is the ending date of search. Must given in YYYY-MM-DD format"
   echo -e "\t  -l | --limit limits the number of responses for the search request to fetch every 2 seconds"
   echo -e "\t  -o | --output-file csvFile must be the name of the csv file to save output to. The output CSV will be saved to ./output directory"
   exit 1 # Exit script after printing help
}

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -s|--source)
      source="$2"
      shift
      shift
      ;;
    -q|--query)
      query="$2"
      shift
      shift
      ;;
    -f|--from-date)
      from_date="$2"
      shift
      shift
      ;;
    -t|--to-date)
      to_date="$2"
      shift
      shift
      ;;
    -l|--limit)
      limit="$2"
      shift
      shift
      ;;
    -o|--output-file)
      output_file="$2"
      shift
      shift
      ;;
    -h|--help)
      helpFunction
      shift
      shift
      ;;
    *)
      # Unknown option
      echo "Unknown option: $1"
      helpFunction
      exit 1
      ;;
  esac
done


# Check if mandatory options are provided
################################################
if [ -z "$source" ] || [ -z "$query" ] || [ -z "$from_date" ] || [ -z "$to_date" ] || [ -z "$output_file" ]; then
  echo "source, query, from_date, to_date, output_file and output_file options are mandatory. Please provide values for all of these options."
  exit 1
fi

# Validate source option
################################################
case $source in
  Iltalehti|Ilta-Sanomat|Helsingin\ Sanomat|YLE\ News)
    ;;
  *)
    echo "Invalid value for source. Current options are Iltalehti, Ilta-Sanomat, Helsingin Sanomat, YLE News."
    exit 1
    ;;
esac

# Your logic for processing the options goes here
echo "Processing options..."
echo "  Source: $source"
echo "  Query: $query"
echo "  From Date: $from_date"
echo "  To Date: $to_date"
echo "  Limit: $limit"
echo "  Output File: ./output/$output_file" 


####################################################################
# Run scrape code according to argument
####################################################################

# Get the right query script
################################################
if [ "$source" == "YLE News" ]; then
  query_python_script="scripts/query_yle.py"
elif [ "$source" == "Iltalehti" ]; then
  query_python_script="scripts/query_il.py"
elif [ "$source" == "Ilta-Sanomat" ]; then
  query_python_script="scripts/query_is.py"
else
  query_python_script="scripts/query_hs.py"
fi

echo "Article listing query script is: $query_python_script"

# Get the output file name
################################################
# Using basename and parameter expansion to remove file extension
file_name=$(basename "$output_file")
file_name_without_extension="${file_name%.*}"

echo "Original output_file name: $file_name"
echo "output_file name without extension: $file_name_without_extension"

# Run python scrape scripts
###############################################

echo "Running $query_python_script ..."
python3 $query_python_script -f $from_date -t $to_date -q "$query" -o $output_file -l $limit
echo "DEBUG"
if [ $? -ne 0 ]; then
  echo "Error: $query_python_script failed to execute."
  exit 1
fi

echo "Running scripts/fetch.py ..."
python3 scripts/fetch.py -i $output_file -o $file_name_without_extension.json
if [ $? -ne 0 ]; then
  echo "Error: scripts/fetch.py failed to execute."
  exit 1
fi

echo "Parse text and author for each article. Running scripts/article_parser.py ..."
python3 scripts/article_parser.py -i $file_name_without_extension.json -o $output_file -s "$source"
if [ $? -ne 0 ]; then
  echo "Error: scripts/article_parser.py failed to execute."
  exit 1
fi

echo "Generate output file. Running scripts/merge.py.py ..."
python3 scripts/merge.py -i $output_file -o $output_file
if [ $? -ne 0 ]; then
  echo "Error: scripts/merge.py failed to execute."
  exit 1
fi

