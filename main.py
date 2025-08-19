import os
import json
from requests import Response

from jinja2 import Template
import functions_framework
from wonderwords import RandomWord

from google.cloud import bigquery
from google.oauth2 import service_account

from includes.objects.movie import Movie
from includes.fetchers.imdb_fetcher import IMDBFetcher

def get_random_keywords(count=10):
    r = RandomWord()
    return r.random_words(count, word_min_length=3, word_max_length=12, include_parts_of_speech=["nouns"])

def get_query_params(query_path:str, params:dict):
    with open(query_path, 'r') as file:
        query_template:Template = Template(file.read())
    return query_template.render(params)

def parse_existing_movies(big_query_client, movies:list[Movie], project_id:str) -> list[Movie]:
    ids:list[str] = []
    for movie in movies:
        ids.append(movie.imdb)
    
    constraint:str = "'" + "', '".join(ids) + "'"
    query:str = get_query_params(
        query_path="./queries/process_pipeline/get_movies.sql", 
        params = {
            "project_id" : project_id,
            "movies_id" : constraint
        }
    )
    query_job = big_query_client.query(query)
    rows = query_job.result()
    existing_movies_id:list[str] = []
    for row in rows:
        existing_movies_id.append(row[0])
    
    movies_parsed:list[Movie] = []
    for movie in movies:
        if movie.imdb not in existing_movies_id:
            movies_parsed.append(movie)
    return movies_parsed

@functions_framework.http
def cinema_data_fetcher(request):
    try:
        # BigQuery API auth
        parameters:dict
        with open('client_secret.json') as json_file:
            parameters = json.load(json_file)
        credentialsPath = os.path.join(os.path.dirname(__file__), 'client_secret.json')
        credentials = service_account.Credentials.from_service_account_file(credentialsPath)
        client = bigquery.Client(credentials=credentials)

        movie_fetcher:IMDBFetcher = IMDBFetcher(domain="https://imdb.iamidiotareyoutoo.com")
        keywords = get_random_keywords(10)
        movies:list[Movie] = []
        for keyword in keywords:
            movies += movie_fetcher.search(query=keyword)
        movies:list[Movie] = parse_existing_movies(big_query_client=client, movies=movies, project_id=parameters["project_id"])
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
                return {"error": f"Failed to insert movies:"}, 500
            
            #  Save casts
            errors = client.insert_rows_json(table_ref_casts, movie_actors)
            if errors:
                print("#"*5 , "CASTS", "#"*5, errors)
                return {"error": f"Failed to insert casts:"}, 500
                    
            return {
                "status": "success",
                "message": f"Processed {len(movies)} movies with {len(movie_actors)} actors",
                "keywords": keywords
            }, 200
    except Exception as e:
        print(e)
        return {
            "error": str(e)
        }, 500
    return "Failed"

if __name__ == "__main__":
    cinema_data_fetcher(None)
