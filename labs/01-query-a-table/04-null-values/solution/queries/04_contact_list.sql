SELECT id, name, COALESCE(NULLIF(email, ''), 'sin correo') AS email
FROM members;
