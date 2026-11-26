SELECT id, title, salary_usd
FROM jobs
WHERE salary_usd > (
    SELECT MAX(salary_usd)
    FROM jobs
    WHERE company_id = 1
);
