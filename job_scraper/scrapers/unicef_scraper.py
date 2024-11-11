from job_scraper.scraper_base import BaseScraper
from job_scraper.models import Job
from job_scraper.database import SessionLocal
from datetime import datetime
import re

class UnicefJobScraper(BaseScraper):
    def parse_jobs(self):
        """Specific parsing logic for UNICEF job site."""
        jobs = []
        session = SessionLocal()

        # Find all job listings by targeting the relevant div
        job_listings = self.soup.find_all('div', class_='row-content--text-info')
        
        for job in job_listings:
            try:
                # Job Title and URL
                title_tag = job.find_all('h4').find('a', class_='job-link')
                title = title_tag.text.strip()
                url = "https://jobs.unicef.org" + title_tag['href']  # Construct full URL
                
                # Location
                location = job.find_all('span', class_='location').text.strip()
                
                # Apply By Date
                date_tag = job.find_all('span', class_='close-date').find('time')
                apply_by_str = date_tag['datetime'] if date_tag else ""
                apply_by = datetime.strptime(apply_by_str, '%Y-%m-%dT%H:%M:%SZ').date()  # Convert to date format
                
                # Check if the job already exists in the database
                existing_job = session.query(Job).filter_by(title=title, location=location, apply_by=apply_by, url=url).first()
                if not existing_job:
                    # Save the job to the database
                    new_job = Job(
                        title=title,
                        post_level='P3',
                        apply_by=apply_by,
                        location=location,
                        url=url
                    )
                    session.add(new_job)
                    session.commit()

                jobs.append({
                    'title': title,
                    'post_level': 'P3',
                    'apply_by': apply_by,
                    'location': location,
                    'url': url
                })

            except (AttributeError, IndexError, ValueError):
                # Skip rows that don't have the expected structure
                continue
        
        session.close()
        return jobs
