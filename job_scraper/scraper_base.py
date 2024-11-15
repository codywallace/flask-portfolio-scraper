import requests
from bs4 import BeautifulSoup
import random
from config import HEADERS_LIST

class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.headers_list = HEADERS_LIST
        self.soup = None
        
    def fetch_page(self):
        # Fetch the page and create a BeautifulSoup object from the given URL
        
        headers = {
            'User-Agent': random.choice(self.headers_list),
            'Referer': "https://www.careers.un.org"
        }
        
        try:
            # Pass the headers in the request
            response = requests.get(self.url, headers=headers)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Failed to fetch the page. Status code: {response.status_code}")
                self.soup = None
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
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
            print("Failed to retrieve the page. Cannot scrape jobs.")
            return []
