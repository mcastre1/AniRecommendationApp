from typing import List, Optional
from pydantic import BaseModel

# Pydantic models
class AnimeCreate(BaseModel):
    mal_id: int
    title: str
    images: Optional[List[dict]] = None
    genres: Optional[List[dict]] = None
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
    images: Optional[List[dict]] = None
    genres: Optional[List[dict]] = None
    episodes: Optional[int] = None
    rating: Optional[str] = None
    synopsis: Optional[str] = None
    year: Optional[int] = None
    themes: Optional[List[dict]] = None

    model_config = {
        "from_attributes": True}
