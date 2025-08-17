-- Step #2 : Create table to store the movies data
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

    PRIMARY KEY (imdb) NOT ENFORCED
);

-- Casts table
CREATE TABLE IF NOT EXISTS {{ project_id }}.cinema_industry_schema.casts (
    movie_id STRING,
    actor_name STRING,

    PRIMARY KEY (movie_id, actor_name) NOT ENFORCED,
    FOREIGN KEY (movie_id) REFERENCES cinema_industry_schema.movies(imdb) NOT ENFORCED
);
