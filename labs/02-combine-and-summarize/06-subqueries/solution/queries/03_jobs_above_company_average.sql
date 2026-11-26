SELECT j.id, j.title, j.salary_usd
FROM jobs AS j
WHERE j.salary_usd > (
    SELECT AVG(o.salary_usd)
    FROM jobs AS o
    WHERE o.company_id = j.company_id
);
