from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from job_scraper.models import Base, Job

# Use a separate test database
TEST_DATABASE_URL = 'sqlite:///test_jobs.db'
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def init_test_db():
    Base.metadata.drop_all(bind=test_engine)  # Drop all tables before test
    Base.metadata.create_all(bind=test_engine)  # Recreate all tables

def clear_test_db():
    session = TestSessionLocal()
    session.query(Job).delete()
    session.commit()
    session.close()

def test_database_init():
    init_test_db()  # Set up the test database
    session = TestSessionLocal()
    assert session.query(Job).count() == 0  # Check that the jobs table is empty
    session.close()

def test_job_insert():
    clear_test_db()  # Clear test database
    session = TestSessionLocal()
    new_job = Job(
        title='Test Job',
        post_level='P3',
        apply_by='2024-01-01',
        location='New York',
        url='http://example.com'
    )
    session.add(new_job)
    session.commit()

    # Check that the job was inserted
    job_count = session.query(Job).count()
    assert job_count == 1

    session.close()
