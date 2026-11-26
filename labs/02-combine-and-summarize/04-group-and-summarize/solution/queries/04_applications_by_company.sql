SELECT c.name AS company, COUNT(a.id) AS applications
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN applications AS a ON a.job_id = j.id
GROUP BY c.id, c.name;
