from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

#Step one: set up the base class.
Base = declarative_base()

#Step two: define the Job model that maps to the 'jobs' table in the database.
class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    post_level = Column(String, nullable=False)
    apply_by = Column(String, nullable=False)
    location = Column(String, nullable=False)
    url = Column(String, nullable=False)
    
