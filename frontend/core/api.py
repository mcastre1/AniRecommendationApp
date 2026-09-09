import requests


def fetch_data():
    response = requests.get('http://127.0.0.1:8000/animes')
    return response.json()

def get_recommendations(liked_animes):
    response = requests.post('http://127.0.0.1:8000/recommendations', json=liked_animes)
    return response.json()

def get_anime_page(page_number):
    response = requests.get(f'https://api.tenrai.org/v1/anime?page={page_number}&limit=50')
    return response.json()

def search_animes(query):
    response = requests.get(f'http://127.0.0.1:8000/animes/search?query={query}')
    return response.json()