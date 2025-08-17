import json
import requests
from requests import Request, Response

from includes.objects.movie import Movie

class IMDBFetcher:

    api_domain:str
    def __init__(self, domain:str = "https://imdb.iamidiotareyoutoo.com"):
        self.api_domain = domain

    def search(self, query:str):
        # Fetch data
        movie_name:str = "American-Psycho"
        response:Response = requests.get(
            f"{self.api_domain}/search?q={movie_name}",
            headers={}
        )
        movies:list[Movie] = []
        if response.status_code == 200:
            # Get the data
            data:dict = response.json()
            # Transform the raw data into Movie objects
            for dict in data["description"]:
                movies.append(Movie(dict))
        return movies
