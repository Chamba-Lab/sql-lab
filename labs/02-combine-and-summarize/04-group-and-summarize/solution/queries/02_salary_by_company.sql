SELECT c.name AS company, COUNT(*) AS jobs, AVG(j.salary_usd) AS avg_salary
FROM companies AS c
JOIN jobs AS j ON j.company_id = c.id
GROUP BY c.id, c.name;
