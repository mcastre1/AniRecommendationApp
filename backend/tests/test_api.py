from fastapi.testclient import TestClient
import sys
import os

# Add backend/src to PYTHONPATH manually
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from main import app

client = TestClient(app)

# Test for succesful anime creation
def test_create_anime():
     # Anime payload for creating a new anime item
    payload = {
        "mal_id": 1,
        "title": "Test Anime",
        "episodes": 12,
        "rating": "PG-13",
        "synopsis": "Test synopsis",
        "year": 2020,
        "genre": [
            {"mal_id": 1, "type": "anime", "name": "Action", "url": "https://example.com"}
        ],
        "themes": [
            {"mal_id": 50, "type": "anime", "name": "Adventure", "url": "https://example.com"}
        ]
    }
    
    # Succesful anime creation
    response = client.post('/animes', json=payload)
    assert response.status_code == 200
    
    # We make sure we can get the newly created anime and check it has the right title.
    response = client.get('/animes/1')
    data = response.json()
    assert data['title'] == 'Test Anime'
    
# Testing getting an anime
def test_get_anime():
    response = client.get('/animes/1')
    assert response.status_code == 200
    
    # We know we have 1 anime row, with Test Anime title at this point, so we check it
    assert response.json()['title'] == 'Test Anime'    

# Test for succesful anime update with id 1
def test_put_anime():
    payload = {
            "mal_id": 1,
            "title": "Test Put Anime",
            "episodes": 134,
            "rating": "PG-13",
            "synopsis": "Test put synopsis",
            "year": 2020,
            "genre": [
                {"mal_id": 1, "type": "anime", "name": "Action", "url": "https://example.com"}
            ],
            "themes": [
                {"mal_id": 50, "type": "anime", "name": "Adventure", "url": "https://example.com"}
            ]
        }
    
    response = client.put('/animes/1', json=payload)
    assert response.status_code == 200
    
    # Get anime object with id 1
    response = client.get('/animes/1')
    data = response.json()
    
    # Make sure anime with id 1 was correctly updated
    assert data['title'] == 'Test Put Anime'

# Test deleting an anime row
def test_delete_anime():
    response = client.delete('/animes/1')
    assert response.status_code == 200
    
    # Checking if anime with id 1 was deleted
    response = client.get('/animes/1')
    assert response.status_code == 404
