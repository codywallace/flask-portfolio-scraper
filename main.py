from flask import Flask, render_template
from job_scraper.scrapers.undp_scraper import UndpJobScraper
from job_scraper.scrapers.unicef_scraper import UnicefJobScraper
from job_scraper.database import init_db, SessionLocal
from job_scraper.models import Job
from datetime import date

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/undp-jobs')
def undp_jobs():
    # Scrape jobs and store them in the database
    scraper = UndpJobScraper('https://jobs.undp.org/cj_view_jobs.cfm')
    scraper.scrape_jobs()

    # Fetch jobs from the database to display in the template
    session = SessionLocal()
    today = date.today()
    jobs = session.query(Job).filter(Job.apply_by >= today).all()
    session.close()

    return render_template('jobs_template.html', jobs=jobs, source='UNDP', post_level='P3')

@app.route('/unicef-jobs')
def unicef_jobs():
    # Scrape jobs and store them in the database
    scraper = UnicefJobScraper('https://jobs.unicef.org/en-us/filter/?search-keyword=&pay-scale=p-3')
    scraper.scrape_jobs()
    
    # Fetch jobs from the database to display in the template
    session = SessionLocal()
    today = date.today()
    jobs = session.query(Job).filter(Job.apply_by >= today).all()
    session.close()
    
    return render_template('jobs_template.html', jobs=jobs, source='UNICEF', post_level='P3')

if __name__ == '__main__':
    app.run(debug=True)
