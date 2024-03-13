from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create the base class for declarative models
Base = declarative_base()

# Define the Url table model
class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    original_url = Column(String)
    short_url = Column(String)
    title = Column(String)
    count = Column(Integer, default=0)
