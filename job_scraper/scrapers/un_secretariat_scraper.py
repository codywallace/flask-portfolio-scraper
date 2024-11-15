from job_scraper.scraper_base import BaseScraper
from job_scraper.models import Job
from job_scraper.database import SessionLocal
from datetime import datetime
import re

class UnSecretariatScraper(BaseScraper):
    def parse_jobs(self):
        
        jobs = []
        session = SessionLocal()
        
        job_listings = self.soup.find_all('div', class_='card border-0 ng-star-inserted')
        
        for job in job_listings:
            # Job Title
            try:
                title = job.find('h2', class_='jbOpen_title').text.strip()

                post_level = job.find(text="Category and Level").find_next('span').text.strip()

                # Duty Station
                location = job.find(text="Duty Station").find_next('span').text.strip()

                # Department/Office
                department_office = job.find(text="Department/Office").find_next('span').text.strip()

                # Deadline
                deadline_str = job.find(text="Deadline").find_next('span').text.strip()
                apply_by = datetime.strptime(deadline_str, '%b %d, %Y').date()  # Convert to date

                # Job Description URL
                job_url = job.find('a', class_='btn btn-primary rounded-0 mt-2')['href']
                
                existing_job = session.query(Job).filter_by(title=title, location=location, apply_by=apply_by, url=job_url).first()
                if not existing_job:
                    new_job = Job(
                        title=title,
                        post_level=post_level,
                        apply_by=apply_by,
                        location=location,
                        url=job_url,
                        source=department_office
                    )
                    session.add(new_job)
                    session.commit()
                    
                jobs.append({
                    'title': title,
                    'post_level': post_level,
                    'apply_by': apply_by,
                    'location': location,
                    'url': job_url
                })
            
            except (AttributeError, IndexError, ValueError):
                continue
            
        session.close()
        return jobs