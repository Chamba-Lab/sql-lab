SELECT jobs.id, jobs.title, companies.name AS company, companies.sector
FROM jobs
JOIN companies ON jobs.company_id = companies.id;
