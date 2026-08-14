from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import AnimeResponse, AnimeCreate
from database import SessionLocal
from crud import get_anime, create_anime, update_anime, delete_anime

router = APIRouter()

# Get the local database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# API endpoints packed up in router to be included in the main FastAPI app. 
# Each endpoint corresponds to a CRUD operation for the Anime model, except root endpoint which is just a welcome message.
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

@router.post('/recommendations', response_model=list[int])
def get_recommendations_endpoint(ids: list[int], db: Session = Depends(get_db)):
    print(f"Received IDs for recommendations: {ids}")  # Debugging statement to log the received IDs
    print("test")
    return ids