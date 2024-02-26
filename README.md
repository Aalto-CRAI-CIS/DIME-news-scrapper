# DIME modified news scrawler

## Use case
This news scrawler is a modified version of the [Finnish media scraper](https://github.com/hsci-r/finnish-media-scrapers). The data structure is modified to fits the requirement of DIME project. The data structure for our use case is as follow: 

| Attribute | Data type |Computed |Explain                      | 
|-----------|-----------|---------|-----------------------------|
| id        | str       |         | id of a news article        |
| feedId    | str       |         | id of live thread feeds     |
| articleId | str       | t       | either id or feed_id        |
| source    | str       |         | name of news agent          |
| url       | str       |         | url                         |
| createdAt | date      |         | original created date       |
| updatedAt | date      |         | modified date of article    |
| type      | str       |         | default: article            |
| headline  | str       |         | headline of article         |
| author    | [str]     |         | list of author names        |
| text      | str       |         | content of article          |

Moreover, we want to save the meta-data for each scrape. The data structure for meta data is as follow:
| Attribute | Data type |Explain                                | 
|-----------|-----------|---------------------------------------|
| scrape_id | str       | a uuid of a scrape                    |
| date      | date      | a timestamp for the scrape            |
| url       | str       | the URL of the API query              |
| source    | str       | name of the news agent                |
| query     | str       | query str used for scraping           |
| n_articles| int       | the total number of articles scrapped |

## News agents
Similar to the original [Finnish media scraper](https://github.com/hsci-r/finnish-media-scrapers), this script target YLE, Iltalehti, Iltasanoma, and Helsinki Sanoma.


## Use Guide

Given all the parameter, the scrapper will extract all articles, save it to output file specified by users. The meta-data will be save in form `<output-file-name>`-meta.csv
```
    scrape  --source yle \
            --query ukraina \
            --from_date YYYY-MM-DD \
            --to_date YYYY-MM-DD \
            --limit 100 \
            --output-file out.csv
```

NOTE: YLE API keys are required to query full article from their API. Create a copy of `.env-sample`, add YLE API keys, and rename the file to `.env`

### Run on triton

1. Create a conda environment and install required packages
`conda env create --file conda-venv.yml`

2. Run `sbatch submit.sh`