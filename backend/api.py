from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import AnimeResponse, AnimeCreate
from database import SessionLocal
from crud import get_anime, create_anime, update_anime, delete_anime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/')
def root_endpoint():
    return {"message": "Welcome to the SQLite FastAPI!"}

@router.post('/animes/', response_model=AnimeResponse)
def create_anime_endpoint(anime: AnimeCreate, db: Session = Depends(get_db)):
    return create_anime(anime, db)

@router.get('/animes/{mal_id}', response_model=AnimeResponse)
def get_anime_endpoint(mal_id: int, db: Session = Depends(get_db)):
    return get_anime(mal_id, db)

@router.put('/animes/{mal_id}', response_model=AnimeResponse)
def update_anime_endpoint(mal_id: int, anime: AnimeCreate, db: Session = Depends(get_db)):
    return update_anime(mal_id, anime, db)

@router.delete('/animes/{mal_id}')
def delete_anime_endpoint(mal_id: int, db: Session = Depends(get_db)):
    return delete_anime(mal_id, db)
