# Web scraping for "[El universal](https://www.eluniversal.com)" news

[![Tests](https://github.com/AnomanderRK/newsscraping/actions/workflows/tests.yml/badge.svg)](https://github.com/AnomanderRK/newsscraping/actions/workflows/tests.yml)

web scraping for different news sites. It retrieves the latest news from the site and stores them in a new folder in your working directory

## Output
- First stage output (Extract) -> csv: Each day will be stored in a new .csv, in a separated folder with the following structure: output/
[site]/[day]/__consolidated_news.csv

- Second stage output (Transform) -> pkl: Some natural language processing is performed using _NLTK_ library. The output will be
stored inside a consolidated pkl file: output/transform.pkl

- Third stage output (load): -> sqlite: The information from previous stages is stored and updated in a general db
in: output/newspaper.db

## How to use it
Note: It is common for different sites to change some of their html structure 
if you find that the code is not working for you, maybe you need to check the **queries** expressions used in the configuration.yaml

 run the following command from your terminal
````cmd
python run_pipeline.py --config_file config.yaml
````

It is possible to run each stage individually from news_scraping/[stage]/main.py

### Requirement
I included the [requirements.txt](requirements.txt) so you can install all the needed packages
