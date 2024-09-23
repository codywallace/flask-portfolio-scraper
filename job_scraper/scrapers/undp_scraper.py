from job_scraper.scraper_base import BaseScraper
from job_scraper.models import Job
from job_scraper.database import SessionLocal
import re
from datetime import datetime

class UndpJobScraper(BaseScraper):
    def parse_jobs(self):
        #Specific parsing logic for UNDP job site.
        jobs = []
        session = SessionLocal()

        job_listings = self.soup.find_all('a', class_='vacanciesTableLink')
        
        for job in job_listings:
            
            try:
                # Job title and URL
                url = job['href']
                title = job.find_all('div', class_='vacanciesTable__cell')[0].find('span').text.strip()
                title = re.sub(r'^\*\s*', '', title) #Remove leading '*' and extra spaces
                
                #Post Level
                post_level = job.find_all('div', class_='vacanciesTable__cell')[2].find('span').text.strip()
                
                #Apply by date
                apply_by = job.find_all('div', class_='vacanciesTable__cell')[3].find('span').text.strip()
                #Convert date to ISO format
                apply_by = datetime.strptime(apply_by, '%b-%d-%y').date()
                
                #Location
                location = job.find_all('div', class_='vacanciesTable__cell')[5].find('span').text.strip()
                
                #Only collect jobs where Post Level is 'P3'
                if post_level in ['P3', 'IPSA-10', 'International Consultant']:
                    #Check if the job already exists in the database
                    existing_job = session.query(Job).filter_by(title=title, location=location, apply_by=apply_by, url=url).first()
                    if not existing_job:
                        #Save the job to the database
                        new_job = Job(
                            title=title,
                            post_level=post_level,
                            apply_by=apply_by,
                            location=location,
                            url=url
                        )
                        session.add(new_job)
                        session.commit()
                        
                    jobs.append({
                        'title': title,
                        'post_level': post_level,
                        'apply_by': apply_by,
                        'location': location,
                        'url': url
                    })
            except (IndexError, AttributeError):
                #Skip rows that don't have the expected structure
                continue
            
        session.close()    
        return jobs