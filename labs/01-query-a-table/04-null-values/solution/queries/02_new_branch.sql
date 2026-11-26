SELECT id, name, district
FROM members
WHERE district <> 'Miraflores' OR district IS NULL;
