from typing import List, Optional
from pydantic import BaseModel

# Pydantic models for image objects
class ImageFormat(BaseModel):
    image_url: Optional[str] = None
    small_image_url: Optional[str] = None
    large_image_url: Optional[str] = None

class AnimeImages(BaseModel):
    jpg: Optional[ImageFormat] = None
    webp: Optional[ImageFormat] = None
##################################

# Pydantic models
class AnimeCreate(BaseModel):
    mal_id: int
    title: str
    images: Optional[AnimeImages] = None
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
    images: Optional[AnimeImages] = None
    genres: Optional[List[dict]] = None
    episodes: Optional[int] = None
    rating: Optional[str] = None
    synopsis: Optional[str] = None
    year: Optional[int] = None
    themes: Optional[List[dict]] = None

    model_config = {
        "from_attributes": True}
