from flask import Flask, render_template
from job_scraper.scrapers.undp_scraper import UndpJobScraper
from job_scraper.database import init_db, SessionLocal
from job_scraper.models import Job

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/')
def home():
    # Scrape jobs and store them in the database
    scraper = UndpJobScraper('https://jobs.undp.org/cj_view_jobs.cfm')
    scraper.scrape_jobs()

    # Fetch jobs from the database to display in the template
    session = SessionLocal()
    jobs = session.query(Job).all()
    session.close()

    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
