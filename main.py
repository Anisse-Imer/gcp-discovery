import os
import json
import requests
from requests import Response

from google.cloud import bigquery
from google.oauth2 import service_account

from includes.movie import Movie

try:
    # BigQuery API auth
    parameters:dict
    with open('client_secret.json') as json_file:
        parameters = json.load(json_file)
    credentialsPath = r'client_secret.json'
    credentials = service_account.Credentials.from_service_account_file(credentialsPath)
    client = bigquery.Client(credentials=credentials)

    # Fetch data
    movie_name:str = "American-Psycho"
    response:Response = requests.get(
        f"https://imdb.iamidiotareyoutoo.com/search?q={movie_name}",
        headers={}
    )
    movies:list[Movie] = []
    if response.status_code == 200:
        # Get the data
        data:dict = response.json()
        # json.dump(data, open("data.json ", "w"), indent=4)

        # Transform the raw data into Movie objects
        for dict in data["description"]:
            movies.append(Movie(dict))

    if movies:
        query = f"""
            CALL `{parameters.get("project_id", "")}.database_name.object_name`()
        """
        results = client.query(query).result()
        for row in results:
            print(row)

except Exception as e:
    print(e)
