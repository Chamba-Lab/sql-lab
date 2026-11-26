SELECT id, COALESCE(first_name || ' ' || last_name, first_name) AS full_name
FROM applications;
