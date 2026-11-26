SELECT c.id, c.name
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
WHERE j.id IS NULL;
