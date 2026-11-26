SELECT c.name AS company, j.title
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id;
