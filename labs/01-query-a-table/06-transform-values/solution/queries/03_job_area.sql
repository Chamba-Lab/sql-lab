SELECT id,
       REPLACE(job_code, ' ', '-') AS job_code,
       SUBSTR(job_code, 1, 3) AS area
FROM applications;
