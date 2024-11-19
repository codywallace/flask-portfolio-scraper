
from ..database import init_db, SessionLocal
from ..models import Job
from ..scrapers.un_secretariat_scraper import UnSecretariatScraper
import json

import json
from job_scraper.database import init_db, SessionLocal
from job_scraper.models import Job
from job_scraper.scrapers.un_secretariat_scraper import UnSecretariatScraper
from job_scraper.config import HEADERS_LIST, UN_Secretariat_URL

def test_un_secretariat_scraper():
    # Initialize the database and clear the jobs table
    init_db()
    session = SessionLocal()
    session.query(Job).delete()
    session.commit()
    # Create a scraper object
    url = UN_Secretariat_URL
    scraper = UnSecretariatScraper(url)

    # Scrape the jobs and save to DB
    scraper.scrape_jobs()

    # Query only jobs with the source 'UN Secretariat'
    jobs = session.query(Job).filter_by(source='UN Secretariat').all()

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
