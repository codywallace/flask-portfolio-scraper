import requests
from bs4 import BeautifulSoup
import random
from job_scraper.config import HEADERS_LIST  # Import the headers list from config.py

class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def fetch_page(self):
        # Prepare the headers
        headers = {
            'User-Agent': random.choice(HEADERS_LIST),  # Use the imported headers list
            'Referer': "https://www.careers.un.org"
        }
        
        try:
            # Send the HTTP GET request
            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Failed to fetch the page. Status code: {response.status_code} for URL: {self.url}")
                self.soup = None
        except requests.RequestException as e:
            print(f"Error fetching the page for URL {self.url}: {e}")
            self.soup = None
        
    def parse_jobs(self):
        # Method to be implemented by subclasses for job parsing logic.
        raise NotImplementedError('Subclasses must implement this method')
    
    def scrape_jobs(self):
        # Fetch the page and parse the jobs
        self.fetch_page()
        if self.soup:
            return self.parse_jobs()
        else:
            print(f"Failed to retrieve the page for URL: {self.url}. Cannot scrape jobs.")
            return []
