SELECT c.id, c.name, COUNT(*) AS applications
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
WHERE a.status <> 'rechazada'
GROUP BY c.id, c.name
HAVING COUNT(*) >= 2;
