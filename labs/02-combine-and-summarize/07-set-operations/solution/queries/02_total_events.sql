SELECT COUNT(*) AS events
FROM (
    SELECT posted_on FROM jobs
    UNION ALL
    SELECT applied_on FROM applications
) AS e;
