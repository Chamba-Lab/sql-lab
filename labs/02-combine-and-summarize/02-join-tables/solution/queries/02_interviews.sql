SELECT c.name AS candidate, j.title, a.applied_on
FROM applications AS a
JOIN candidates AS c ON a.candidate_id = c.id
JOIN jobs AS j ON a.job_id = j.id
WHERE a.status = 'entrevista';
