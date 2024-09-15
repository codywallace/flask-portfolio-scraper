import requests
from bs4 import BeautifulSoup

class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        
    def fetch_page(self):
        #Fetch the page and create a BeautifulSoup object from the the given URL
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(self.url)
            response.raise_for_status() #Raise an HTTPError for bad responses
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            self.soup = None
        
    def parse_jobs(self):
        #Method to be implemented by subclasses for job parsing logic.
        raise NotImplementedError('Subclasses must implement this method')
    
    def scrape_jobs(self):
        #Fetch the page and parse the jobs
        self.fetch_page()
        return self.parse_jobs()
    