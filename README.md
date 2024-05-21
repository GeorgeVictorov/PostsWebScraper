# Posts Web Scraper

## Overview

This project is designed to scrape posts from various websites, store the scraped data in an SQLite database, and send
the collected data to specified destinations via APIs.

## Features

* Scraping: The scraper gathers posts from a range of websites.
* Database Storage: Scraped data is efficiently managed and stored using SQLite, ensuring easy access and retrieval.
* API Integration: Collected data can be seamlessly transmitted to designated endpoints via APIs.

## Technologies Used

* [Requests](https://requests.readthedocs.io): For making HTTP requests to fetch website content.
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4): For parsing HTML content and extracting relevant data from web pages.
* [SQLite3](https://docs.python.org/3/library/sqlite3.html): For managing the project's database, providing a lightweight and self-contained solution.