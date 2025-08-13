import json
import requests
from requests import Response

from dotenv import load_dotenv

from includes.movie import Movie

load_dotenv()

# Fetch data from API
search_query:str = "American-Psycho"
response:Response = requests.get(
    f"https://imdb.iamidiotareyoutoo.com/search?q={search_query}"
)

# Save local file
data:dict = response.json()
json.dump(data, open("./data/file.json", "w"), indent = 4)

# Transform each row into an object
movies:list[Movie] = []
for dict in data["description"]:
    movies.append(Movie(dict))

# Print for test purposes
print(movies)
