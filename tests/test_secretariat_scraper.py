import json
from job_scraper.database import init_db, SessionLocal
from job_scraper.models import Job
from job_scraper.scrapers.un_secretariat_scraper import UnSecretariatScraper

def test_un_secretariat_scraper():
    # Initialize the database and clear the jobs table
    init_db()
    session = SessionLocal()
    session.query(Job).delete()
    session.commit()

    # Create a scraper object
    url = 'https://careers.un.org/jobopening?language=en&data=%257B%2522aoe%2522:%255B%255D,%2522aoi%2522:%255B%255D,%2522el%2522:%255B%255D,%2522ct%2522:%255B%255D,%2522ds%2522:%255B%2522NEWYORK%2522%255D,%2522jn%2522:%255B%255D,%2522jf%2522:%255B%255D,%2522jc%2522:%255B%2522PD%2522%255D,%2522jle%2522:%255B%2522100%2522%255D,%2522dept%2522:%255B%255D,%2522span%2522:%255B%255D%257D'
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
