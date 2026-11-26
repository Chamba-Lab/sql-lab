SELECT j.id, j.title, COUNT(*) AS applications
FROM jobs AS j
JOIN applications AS a ON a.job_id = j.id
GROUP BY j.id, j.title
HAVING COUNT(*) >= 2;
