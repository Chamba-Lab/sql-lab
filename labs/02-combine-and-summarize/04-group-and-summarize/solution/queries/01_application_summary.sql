SELECT COUNT(*) AS applications, COUNT(DISTINCT candidate_id) AS candidates, COUNT(DISTINCT job_id) AS jobs,
       MIN(applied_on) AS first_applied, MAX(applied_on) AS last_applied
FROM applications;
