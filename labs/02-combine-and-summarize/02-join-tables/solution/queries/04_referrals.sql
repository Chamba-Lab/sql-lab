SELECT c.name AS candidate, r.name AS recommender
FROM candidates AS c
JOIN candidates AS r ON c.referred_by = r.id;
