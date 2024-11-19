from job_scraper.scraper_base import BaseScraper
from job_scraper.models import Job
from job_scraper.database import SessionLocal
from datetime import datetime

class UnicefJobScraper(BaseScraper):
    def parse_jobs(self):
        """Specific parsing logic for UNICEF job site."""
        jobs = []
        session = SessionLocal()

        # Find all job listings by targeting the relevant div
        job_listings = self.soup.find_all('div', class_='row-content')

        for job in job_listings:
            try:
                # Job Title and URL
                title_tag = job.find('a', class_='job-link')  # Only one title per job
                if not title_tag:
                    continue  # Skip if title is not found
                
                title = title_tag.text.strip()
                url = "https://jobs.unicef.org" + title_tag['href']  # Construct full URL

                # Location
                location_tag = job.find('span', class_='location')
                location = location_tag.text.strip() if location_tag else "Not specified"

                # Apply By Date
                date_tag = job.find('time')
                apply_by_str = date_tag['datetime'] if date_tag else None
                apply_by = (
                    datetime.strptime(apply_by_str, '%Y-%m-%dT%H:%M:%SZ').date()
                    if apply_by_str else None
                )

                # Skip if essential data is missing
                if not title or not apply_by:
                    continue

                # Check if the job already exists in the database
                existing_job = session.query(Job).filter_by(
                    title=title, location=location, apply_by=apply_by, url=url
                ).first()
                if not existing_job:
                    # Save the job to the database
                    new_job = Job(
                        title=title,
                        post_level='P3',  # You may adjust this as needed
                        apply_by=apply_by,
                        location=location,
                        url=url,
                        source='UNICEF'
                    )
                    session.add(new_job)
                    session.commit()

                # Add the job to the jobs list
                jobs.append({
                    'title': title,
                    'post_level': 'P3',
                    'apply_by': apply_by,
                    'location': location,
                    'url': url
                })

            except Exception as e:
                print(f"Error parsing job: {e}")
                continue

        session.close()
        return jobs
