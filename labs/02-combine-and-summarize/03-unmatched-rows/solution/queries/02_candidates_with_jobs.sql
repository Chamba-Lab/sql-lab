SELECT c.id, c.name, j.title
FROM candidates AS c
LEFT JOIN applications AS a ON a.candidate_id = c.id
LEFT JOIN jobs AS j ON a.job_id = j.id;
