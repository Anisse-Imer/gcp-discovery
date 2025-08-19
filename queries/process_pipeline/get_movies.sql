SELECT
  distinct m.imdb
FROM
  {{ project_id }}.cinema_industry_schema.movies as m  
WHERE
  m.imdb IN ( {{ movies_id }} );
