from src.models import Anime
from src.schemas import AnimeCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session

# CRUD operations for the Anime model. 
# These functions interact with the database to perform create, read, update, and delete operations on anime records.
def get_anime( mal_id: int, db: Session):
    anime = db.query(Anime).filter(Anime.mal_id == mal_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    return anime

def create_anime(anime: AnimeCreate, db: Session):
    if db.query(Anime).filter(Anime.mal_id == anime.mal_id).first():
        raise HTTPException(status_code=400, detail="This anime already exists!")
    
    # Create a new Anime instance and add it to the database
    db_anime = Anime(**anime.model_dump())
    
    # Add the new anime to the database
    db.add(db_anime)            # Add the new anime instance to the database sessi  on
    db.commit()                 # Commit the transaction to save the new anime to the database
    db.refresh(db_anime)        # Refresh the instance to get the updated data from the database (e.g., auto-generated fields)
    return db_anime             # Return the newly created anime instance as the response

def update_anime(mal_id: int, anime: AnimeCreate, db: Session):
    db_anime = db.query(Anime).filter(Anime.mal_id == mal_id).first()
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    # Update the anime instance with the new data
    for key, value in anime.model_dump().items():
        setattr(db_anime, key, value)
    
    db.commit()                 # Commit the transaction to save the changes to the database
    db.refresh(db_anime)        # Refresh the instance to get the updated data from the database
    return db_anime             # Return the updated anime instance as the response

def delete_anime(mal_id: int, db: Session):
    db_anime = db.query(Anime).filter(Anime.mal_id == mal_id).first()
    if not db_anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    db.delete(db_anime)          # Delete the anime instance from the database session
    db.commit()                  # Commit the transaction to save the changes to the database
    return {"message": "Anime deleted successfully"} 