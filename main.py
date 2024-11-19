from flask import Flask, render_template
from job_scraper.scrapers.undp_scraper import UndpJobScraper
from job_scraper.scrapers.unicef_scraper import UnicefJobScraper
from job_scraper.scrapers.un_secretariat_scraper import UnSecretariatScraper
from job_scraper.database import init_db, SessionLocal
from job_scraper.models import Job
from job_scraper.config import HEADERS_LIST, UNDP_URL, UNICEF_URL, UN_Secretariat_URL
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
    scraper = UndpJobScraper(UNDP_URL)
    scraper.scrape_jobs()

    # Fetch jobs from the database to display in the template
    session = SessionLocal()
    today = date.today()
    jobs = session.query(Job).filter(Job.apply_by >= today, Job.source == "UNDP").all()
    session.close()

    return render_template('jobs_template.html', jobs=jobs, source='UNDP', post_level='P3')

@app.route('/unicef-jobs')
def unicef_jobs():
    # Scrape jobs and store them in the database
    scraper = UnicefJobScraper(UNICEF_URL)
    scraper.scrape_jobs()
    
    # Fetch jobs from the database to display in the template
    session = SessionLocal()
    today = date.today()
    jobs = session.query(Job).filter(Job.apply_by >= today, Job.source == "UNICEF").all()
    session.close()
    
    return render_template('jobs_template.html', jobs=jobs, source='UNICEF', post_level='P3')

@app.route('/unsecretariat-jobs')
def un_secretariat_jobs():
    # Scrape jobs and store them in the database
    scraper = UnSecretariatScraper(UN_Secretariat_URL)
    scraper.scrape_jobs()
    
    # Fetch jobs from the database to display in the template
    session = SessionLocal()
    today = date.today()
    post_level = 'P3'
    jobs = session.query(Job).filter(Job.apply_by >= today, Job.source == "UN Secretariat").all()
    session.close()
    
    return render_template('jobs_template.html', jobs=jobs, source='UN Secretariat', post_level=post_level)

if __name__ == '__main__':
    app.run(debug=True)
