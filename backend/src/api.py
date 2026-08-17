from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models import Anime
from src.schemas import AnimeResponse, AnimeCreate
from src.database import SessionLocal
from src.crud import get_anime, create_anime, update_anime, delete_anime
import src.states as states
import numpy as np

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


# Extra endpoints for gui operations
# Get top 10 recommended animes from user liked list
@router.post('/recommendations', response_model=list[AnimeResponse])
def get_recommendations_endpoint(ids: list[int], db: Session = Depends(get_db)):
    anime_df = states.anime_df
    feature_matrix = states.feature_matrix
    knn_model = states.knn_model
    
    # We get the vectores from feature_matrix that correspond to the anime ids in the request.
    liked_vectors = feature_matrix[anime_df['mal_id'].isin(ids)]
    
    # We find the indices of the nearest neighbors for each id that was passed in the request, in this case we are looking for 25 nearest neighbors per id.
    distances, indices = knn_model.kneighbors(liked_vectors, n_neighbors=25)
    # Since we are looking at multiple ids, we flatten the indices array and get the unique indices to avoid duplicates.
    recommended_indices = np.unique(indices.flatten())
    # We then get the anime objects from the anime_df with the recommended indices.
    recommended_animes = anime_df.iloc[recommended_indices]
    # And then we filter out the animes that were already liked by the user, so we don't recommend them again.
    recommended_animes = recommended_animes[~recommended_animes['mal_id'].isin(ids)]
    
    # Finally, we return the top 10 recommendations.
    top10 = recommended_animes.head(10)
    return top10.to_dict(orient='records')


# Get anime rows with pagination
@router.get('/animes', response_model=list[AnimeResponse])
def get_animes(page: int = 1, limit: int = 50, db : Session = Depends(get_db)):
    offset = (page - 1) * limit
    animes = db.query(Anime).offset(offset).limit(limit).all()
    
    return animes