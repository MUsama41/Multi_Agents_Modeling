from sqlalchemy import create_all, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Since the original used a specific URI, I'll put it in config later, but for now:
DATABASE_URL = "postgresql://postgres:Gakhar555@database-3.cl8ugeouejun.eu-north-1.rds.amazonaws.com:5432/postgres"

from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class IdeaModel(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True, index=True)
    main_idea = Column(String(200), nullable=True)
    resubmitted_idea = Column(String(200), nullable=True)
    agent_name = Column(String(100), nullable=True)
    generative_num = Column(Integer, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
