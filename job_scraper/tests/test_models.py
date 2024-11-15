from job_scraper.models import Job
from job_scraper.database import SessionLocal

def test_job_model():
    """Test creating a job instance."""
    session = SessionLocal()
    new_job = Job(
        title='Test Job',
        post_level='P3',
        apply_by='2024-01-01',
        location='New York',
        url='http://example.com'
    )
    session.add(new_job)
    session.commit()
    
    job_from_db = session.query(Job).first()
    assert job_from_db.title == 'Test Job'
    session.close()
