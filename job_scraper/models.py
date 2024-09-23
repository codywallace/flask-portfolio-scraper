from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from datetime import date

#Step one: set up the base class.
Base = declarative_base()

#Step two: define the Job model that maps to the 'jobs' table in the database.
class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    post_level = Column(String, nullable=False)
    apply_by = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    url = Column(String, nullable=False)
    
