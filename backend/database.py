from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database setup
engine = create_engine("sqlite:///animes.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)