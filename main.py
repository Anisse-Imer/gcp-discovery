import json
from requests import Response

from google.cloud import bigquery
from google.oauth2 import service_account

from includes.objects.movie import Movie
from includes.fetchers.imdb_fetcher import IMDBFetcher

def main():
    try:
        # BigQuery API auth
        parameters:dict
        with open('client_secret.json') as json_file:
            parameters = json.load(json_file)
        credentialsPath = r'client_secret.json'
        credentials = service_account.Credentials.from_service_account_file(credentialsPath)
        client = bigquery.Client(credentials=credentials)

        movie_fetcher:IMDBFetcher = IMDBFetcher(domain="https://imdb.iamidiotareyoutoo.com")
        movies:list[Movie] = movie_fetcher.search(query="Spider-Man")

        if movies:
            list_movies_dict:list[dict] = []
            movie_actors:list[dict] = []
            for movie in movies:
                movie_dict:dict = movie.to_dict()
                for actor in movie_dict.pop("actors"):
                    if actor != "" :
                        movie_actors.append({
                            "movie_id" : movie_dict["imdb"],
                            "actor_name" : actor
                        })
                list_movies_dict.append(movie_dict)
            # Save movies
            table_ref_movies = client.dataset("cinema_industry_schema").table("movies")
            table_ref_casts = client.dataset("cinema_industry_schema").table("casts")            
            errors = client.insert_rows_json(table_ref_movies, list_movies_dict)
            if errors:
                print("#"*5 , "MOVIES", "#"*5, errors)
            # Save casts
            errors = client.insert_rows_json(table_ref_casts, movie_actors)
            if errors:
                print("#"*5 , "CASTS", "#"*5, errors)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
