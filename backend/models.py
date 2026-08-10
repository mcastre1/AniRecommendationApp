from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Database model
class Anime(Base):
    __tablename__ = "animes"

    mal_id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String, nullable=False)
    genre = Column(JSON)
    episodes = Column(Integer)
    rating = Column(String)
    synopsis = Column(String)
    year = Column(Integer)
    themes = Column(JSON)