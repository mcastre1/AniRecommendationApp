import time
import requests

pages = 607
url = "https://api.tenrai.org/v1/anime?page=1&limit=50"

for page in range(1, pages + 1):
    url = f"https://api.tenrai.org/v1/anime?page={page}&limit=50"
    try:
        response = requests.get(url)
        data = response.json()
        print(data)
    except requests.RequestException as e:
        print(f"Error fetching data for page {page}: {e}")
    time.sleep(1)  # Add a delay of 1 second between requests to avoid overwhelming the server