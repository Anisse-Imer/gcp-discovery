-- Step #2 : Create table to store the movies data
-- Actors table
CREATE TABLE IF NOT EXISTS {{ project_id }}.cinema_industry_schema.actors (
    id INT64,
    name STRING,

    PRIMARY KEY (id) NOT ENFORCED
);
-- Movies table
CREATE TABLE IF NOT EXISTS {{ project_id }}.cinema_industry_schema.movies (    
    imdb STRING,
    title STRING,
    year INT64,
    rank INT64,
    aka STRING,

    imdb_url STRING,
    imdb_iv STRING,
    img_poster STRING,
    photo_width INT64,
    photo_height INT64,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),

    PRIMARY KEY (id) NOT ENFORCED
);
-- Casts table
CREATE TABLE IF NOT EXISTS {{ project_id }}.cinema_industry_schema.casts (
    id INT64,
    movie_id STRING,
    actor_id INT64,

    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (movie_id) REFERENCES cinema_industry_schema.movies(imdb) NOT ENFORCED,
    FOREIGN KEY (actor_id) REFERENCES cinema_industry_schema.actors(id) NOT ENFORCED
);
