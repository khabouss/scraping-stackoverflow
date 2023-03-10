# scraping-stackoverflow
using bs4 (beautifulsoup) to scrap a web page of stackoverflow and put it in ElasticSearch server
the setup.sh will run a docker container with ElasticSearch
and output a file containing the results scraped from the page

# usage
````
sh setup.sh
python scrap.py "link to page" "output file name (without extention)"
````
