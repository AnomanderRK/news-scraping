# Web scraping for "[la republica](https://www.larepublica.co/)" news

web scrapping from 'la republica'. It retrieves the latest news from the site and store them into a new folder 
in your working directory

[![Tests](https://github.com/AnomanderRK/newsscraping/actions/workflows/tests.yml/badge.svg)](https://github.com/AnomanderRK/newsscraping/actions/workflows/tests.yml)

## How to use it
Note: It is common for different sites to change some of their html structure 
if you find that the code is not working for you, maybe you need to check the **xpath** expressions used

 run the following command from your terminal
````cmd
python scraper.py
````

## Dependencies
- lxml -> Look for **[xpath](https://devhints.io/xpath)** expressions
- requests -> Retrieve information from different pages

### Requirement
I included the [requirements.txt](requirements.txt) so you can install all the needed packages