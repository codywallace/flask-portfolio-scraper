import json
from job_scraper.database import init_db, SessionLocal
from job_scraper.models import Job
from job_scraper.scrapers.unicef_scraper import UnicefJobScraper

def test_unicef_scraper():
    # Initialize the database
    init_db()

    # Create a scraper object
    url = 'https://jobs.unicef.org/en-us/filter/?search-keyword=&pay-scale=p-3'
    scraper = UnicefJobScraper(url)

    # Scrape the jobs and save to DB
    scraper.scrape_jobs()

    # Query the database
    session = SessionLocal()
    jobs = session.query(Job).all()

    # Check that the jobs list is not empty
    assert len(jobs) > 0

    # Print the scraped jobs as JSON
    print(f"\nNumber of jobs scraped: {len(jobs)}")
    print("\nList of scraped jobs (JSON format):")
    print(json.dumps([{
        'title': job.title,
        'post_level': job.post_level,
        'apply_by': job.apply_by.strftime('%Y-%m-%d'),  # Convert date to string
        'location': job.location,
        'url': job.url
    } for job in jobs], indent=4))

    session.close()
