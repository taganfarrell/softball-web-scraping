# Softball Web Scraping

Automated the collection of D1 college softball statistics from a d1softball.com using Python, leveraging the Selenium web automation framework and BeautifulSoup library for HTML parsing. 

The main.py file scrapes batting and pitching data for every d1 softball player for every year available and writes them to appropriate csv files for each year.

The scores.py file scrapes game result data by iterating through every team's schedule and extracts all of their home games. This makes sure that there are no duplicates and every single game is accounted for once. This file also loops through each year and creates csv files for each one available on the website.
