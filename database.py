from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Journey(Base):
    __tablename__ = 'journeys'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_location = Column(String)
    end_location = Column(String)
    distance = Column(Float)
    project = Column(String)

class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///mileage_tracker.db', echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_journey(self, start_time, end_time, start_location, end_location, distance, project):
        journey = Journey(
            start_time=start_time,
            end_time=end_time,
            start_location=start_location,
            end_location=end_location,
            distance=distance,
            project=project
        )
        self.session.add(journey)
        self.session.commit()

    def get_journeys(self):
        return self.session.query(Journey).all()