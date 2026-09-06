import requests


def fetch_data():
    response = requests.get('http://127.0.0.1:8000/animes')
    return response.json()

def get_recommendations(liked_animes):
    response = requests.post('http://127.0.0.1:8000/recommendations', json=liked_animes)
    return response.json()