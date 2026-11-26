SELECT id, name
FROM candidates
WHERE id IN (
    SELECT a.candidate_id
    FROM applications AS a
    JOIN jobs AS j ON j.id = a.job_id
    WHERE j.mode = 'remoto'
);
