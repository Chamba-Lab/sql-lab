SELECT id, district, rent
FROM apartments
WHERE district IN ('Miraflores', 'Barranco') AND rent < 2000;
