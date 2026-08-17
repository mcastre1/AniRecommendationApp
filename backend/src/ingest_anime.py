import time
import requests
from backend.src.database import SessionLocal
from backend.src.models import Anime

pages = 607
url = "https://api.tenrai.org/v1/anime?page=1&limit=50"
db = SessionLocal()

for page in range(1, pages + 1):
    url = f"https://api.tenrai.org/v1/anime?page={page}&limit=50"
    try:
        response = requests.get(url)
        data = response.json()
        for a in data.get("data", []):
            anime = Anime(
                mal_id=a.get("mal_id"),
                title=a.get("title"),
                genres=a.get("genres"),
                episodes=a.get("episodes"),
                rating=a.get("rating"),
                synopsis=a.get("synopsis"),
                year=a.get("year"),
                themes=a.get("themes"),
            )
            
            db.add(anime)
            db.commit()
            db.refresh(anime)
            
            #[print(f"Added anime: {anime.title} (MAL ID: {anime.mal_id})")]
        print(f"Page {page} processed successfully.")
        
    except requests.RequestException as e:
        print(f"Error fetching data for page {page}: {e}")
    time.sleep(1)  # Add a delay of 1 second between requests to avoid overwhelming the server