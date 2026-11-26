SELECT c.id, c.name
FROM candidates AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM candidates AS r
    WHERE r.referred_by = c.id
);
