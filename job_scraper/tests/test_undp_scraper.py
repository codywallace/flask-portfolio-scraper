from job_scraper.scrapers.undp_scraper import UndpJobScraper
from job_scraper.database import SessionLocal, init_db
from job_scraper.models import Job 
import json

def test_undp_scraper():
    #Initialize he database
    init_db()
    
    #Create a scraper object
    url = 'https://jobs.undp.org/cj_view_jobs.cfm'
    scraper = UndpJobScraper(url)
    
    #Scrap the jobs and save to DB
    scraper.scrape_jobs()
    
    #Query the database
    session = SessionLocal()
    jobs = session.query(Job).all()
    
    #Check that the jobs list is not empty
    assert len(jobs) > 0
    
    #Print the scraped jobs as JSON

    print(f"\nNumber of jobs scraped: {len(jobs)}")
    print("\nList of scraped jobs (JSON format):")
    print(json.dumps([{
        'title': job.title,
        'post_level': job.post_level,
        'apply_by': job.apply_by,
        'location': job.location,
        'url': job.url
    } for job in jobs], indent=4))
    
    session.close()
    