from fastapi.testclient import TestClient
import sys
import os

# Add backend/src to PYTHONPATH manually
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from main import app

client = TestClient(app)

def test_get_anime():
    response = client.get('/animes')
    assert response.status_code == 405
