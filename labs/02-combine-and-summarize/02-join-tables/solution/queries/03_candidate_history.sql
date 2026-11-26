SELECT j.title, co.name AS company, a.status
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
JOIN jobs AS j ON a.job_id = j.id
JOIN companies AS co ON j.company_id = co.id
WHERE c.id = 6;
