from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="SQLite FastAPI")

# Database setup
engine = create_engine("sqlite:///animes.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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

Base.metadata.create_all(bind=engine)

# Pydantic models
class AnimeCreate(BaseModel):
    mal_id: int
    title: str
    genre: Optional[List[dict]] = None
    episodes: Optional[int] = None
    rating: Optional[str] = None
    synopsis: Optional[str] = None
    year: Optional[int] = None
    themes: Optional[List[dict]] = None

# Response model for returning anime data
# We dont really have anything private, so we return everything
class AnimeResponse(BaseModel):
    mal_id: int
    title: str
    genre: Optional[List[dict]] = None
    episodes: Optional[int] = None
    rating: Optional[str] = None
    synopsis: Optional[str] = None
    year: Optional[int] = None
    themes: Optional[List[dict]] = None

    model_config = {
        "from_attributes": True}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()

@app.get('/')
def root():
    return {"message": "Welcome to the SQLite FastAPI!"}

@app.get("/animes/{mal_id}", response_model=AnimeResponse)
def get_anime( mal_id: int, db: Session = Depends(get_db)):
    anime = db.query(Anime).filter(Anime.mal_id == mal_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    return anime

@app.post("/animes/", response_model=AnimeResponse)
def create_anime(anime: AnimeCreate, db: Session = Depends(get_db)):
    if db.query(Anime).filter(Anime.mal_id == anime.mal_id).first():
        raise HTTPException(status_code=400, detail="This anime already exists!")
    
    # Create a new Anime instance and add it to the database
    db_anime = Anime(**anime.model_dump())
    
    # Add the new anime to the database
    db.add(db_anime)            # Add the new anime instance to the database session
    db.commit()                 # Commit the transaction to save the new anime to the database
    db.refresh(db_anime)        # Refresh the instance to get the updated data from the database (e.g., auto-generated fields)
    return db_anime             # Return the newly created anime instance as the response

@app.put("/animes/{mal_id}", response_model=AnimeResponse)
def update_anime(mal_id: int, anime: AnimeCreate, db: Session = Depends(get_db)):
    db_anime = db.query(Anime).filter(Anime.mal_id == mal_id).first()
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    # Update the anime instance with the new data
    for key, value in anime.model_dump().items():
        setattr(db_anime, key, value)
    
    db.commit()                 # Commit the transaction to save the changes to the database
    db.refresh(db_anime)        # Refresh the instance to get the updated data from the database
    return db_anime             # Return the updated anime instance as the response

@app.delete("/animes/{mal_id}")
def delete_anime(mal_id: int, db: Session = Depends(get_db)):
    db_anime = db.query(Anime).filter(Anime.mal_id == mal_id).first()
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    db.delete(db_anime)          # Delete the anime instance from the database session
    db.commit()                  # Commit the transaction to save the changes to the database
    return {"message": "Anime deleted successfully"} 