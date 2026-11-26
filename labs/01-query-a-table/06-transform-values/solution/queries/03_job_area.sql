SELECT id,
       replace(job_code, ' ', '-') AS job_code,
       substr(job_code, 1, 3) AS area
FROM applications;
