SELECT c.name AS company, SUM(j.salary_usd) AS total_salary, SUM(per_job.applications) AS applications
FROM companies AS c
JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN (
    SELECT job_id, COUNT(*) AS applications
    FROM applications
    GROUP BY job_id
) AS per_job ON per_job.job_id = j.id
GROUP BY c.id, c.name;
