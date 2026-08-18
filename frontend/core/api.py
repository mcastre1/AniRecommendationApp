import requests


def fetch_data():
    response = requests.get('http://127.0.0.1:8000/animes')
    return response.json()