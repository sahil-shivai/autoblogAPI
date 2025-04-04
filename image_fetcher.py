import requests
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def fetch_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": PEXELS_API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["large"]
    return None


if __name__ == "__main__":
    print(fetch_image("Python Programming"))
