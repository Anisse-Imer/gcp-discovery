SELECT
  c.*,
  m.title
FROM
  `striking-talent-462114-d2.cinema_industry_schema.casts` as c
LEFT JOIN `striking-talent-462114-d2.cinema_industry_schema.movies` as m ON m.imdb = c.movie_id;
