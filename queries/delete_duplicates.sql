select
  count(*) as nb_occ,
  c.actor_name,
  c.movie_id
from
    {{ project_id }}.cinema_industry_schema.casts as c
GROUP BY
  c.actor_name, c.movie_id
ORDER BY nb_occ desc;

SELECT
  count(*) as nb_occ,
  m.imdb as imdb
FROM
  {{ project_id }}.cinema_industry_schema.movies as m
GROUP BY
  imdb
ORDER BY nb_occ desc;

CREATE OR REPLACE TABLE {{ project_id }}.cinema_industry_schema.casts AS
SELECT DISTINCT *
FROM {{ project_id }}.cinema_industry_schema.casts;

CREATE OR REPLACE TABLE {{ project_id }}.cinema_industry_schema.movies AS
SELECT DISTINCT * EXCEPT(created_at), CURRENT_TIMESTAMP() AS created_at
FROM {{ project_id }}cinema_industry_schema.movies;
